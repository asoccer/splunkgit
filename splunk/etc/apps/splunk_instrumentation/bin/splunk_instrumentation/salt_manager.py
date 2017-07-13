import uuid
import splunk_instrumentation.splunklib as splunklib
import splunk_instrumentation.constants as constants
from splunk_instrumentation.splunklib.data import Record


# Salt Lifecycle:
# - On Splunk start @ swa-eligible node (search head, or single instance):
#   + Sync with cluster master (CM salt overwrites any existing local salt)
#   + Still no salt? Generate a new one, stick it in the conf file.
#   + Conf replication fairies take it from there.
# - On demand / on read (i.e. when requested to inject into swajs, etc)
#   + Read from conf file
#   + No salt in the conf file? Generate a new one
#   + Can't guarantee write access in this context due to user permissions,
#     so we can't write it back to the conf file
#   + At least attempt to use the same temporary salt until the next sync
# - On scripted input run (nightly)
#   + Sync with the cluster master (CM salt overwrite any existing local salt)

# Used when a salt cannot be found, or persisted to the conf file
temporary_salt = None


class SaltManager(object):

    # Static
    salt = None

    # Instance
    services = None
    
    def __init__(self, services):
        self.services = services

    def get_salt(self):
        global temporary_salt
        
        if self.salt is not None:
            return self.salt
        
        self.salt = self.services.telemetry_conf_service.content.get('telemetrySalt')
        
        # Unlike the deployment ID - which we do not bother to generate
        # if we cannot write it to the conf file - there *must* be a salt
        # to ensure anonymization of PII. So, even if we can't persist it,
        # we'll generate a one-time-only salt.
        #
        # Note: We sync with the cluster master at splunk startup,
        #       as well as each night during the scripted input run.
        if not self.salt:
            self.salt = temporary_salt or self.generate_salt()
            if self.services.telemetry_conf_service.is_read_only:
                temporary_salt = self.salt
            else:
                try:
                    self.write_salt_to_conf_file()
                except:
                    temporary_salt = self.salt

        return self.salt

    def sync_with_cluster(self):
        try:
            cm_salt = None
            
            resp = self.services.splunkd.request(
                constants.ENDPOINTS['MASTER_SETTINGS'],
                method='GET',
                owner='nobody',
                app=constants.INST_APP_NAME)
            data = splunklib.data.load(resp.get('body').read())
            entry = data['feed'].get('entry')
            if entry:
                if type(entry) is list:
                    salt_list = [value['content'].get('telemetrySalt') for value in entry]
                    if salt_list:
                        salt_list.sort()
                        cm_salt = salt_list[0]
                elif type(entry) is Record:
                    cm_salt = entry['content'].get('telemetrySalt')

            if cm_salt:
                self.salt = cm_salt
                self.write_salt_to_conf_file()
        except:
            # Best effort only
            pass

    def generate_salt(self):
        self.salt = uuid.uuid4()
        self.write_salt_to_conf_file()
        return self.salt

    def write_salt_to_conf_file(self):
        self.services.telemetry_conf_service.update({
            'telemetrySalt': self.salt
        })
        
