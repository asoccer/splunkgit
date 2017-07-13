#   Version 6.6.2
#
############################################################################
# OVERVIEW
############################################################################
# This file contains descriptions of the settings that you can use to
# configure limitations for the search commands.
#
# Each stanza controls different search commands settings.
#
# There is a limits.conf file in the $SPLUNK_HOME/etc/system/default/ directory.
# Never change or copy the configuration files in the default directory. 
# The files in the default directory must remain intact and in their original 
# location.
#
# To set custom configurations, create a new file with the name limits.conf in 
# the $SPLUNK_HOME/etc/system/local/ directory. Then add the specific settings
# that you want to customize to the local configuration file.
# For examples, see limits.conf.example. You must restart the Splunk instance 
# to enable configuration changes.
#
# To learn more about configuration files (including file precedence) see the
# documentation located at
# http://docs.splunk.com/Documentation/Splunk/latest/Admin/Aboutconfigurationfiles
#
# About Distributed Search
#   Unlike most settings which affect searches, limits.conf settings are not
#   provided by the search head to be used by the search peers.  This means
#   that if you need to alter search-affecting limits in a distributed
#   environment, typically you will need to modify these settings on the
#   relevant peers and search head for consistent results.
#
############################################################################
# GLOBAL SETTINGS 
############################################################################
# Use the [default] stanza to define any global settings.
#   * You can also define global settings outside of any stanza, at the top of
#     the file.
#   * Each .conf file should have at most one default stanza. If there are
#     multiple default stanzas, settings are combined. In the case of
#     multiple definitions of the same setting, the last definition in the
#     file takes precedence.
#   * If a setting is defined at both the global level and in a specific
#     stanza, the value in the specific stanza takes precedence.
#
# CAUTION: Do not alter the settings in the limits.conf file unless you know 
#     what you are doing.  Improperly configured limits might result in   
#     splunkd crashes, memory overuse, or both.


[default]

DelayArchiveProcessorShutdown = <bool>
* Specifies whether during splunk shutdown archive processor should finish 
  processing archive file under process. 
* When set to “false”: The archive processor abandons further processing of 
  the archive file and will process again from start again.
* When set to “true”: The archive processor will complete processing of
  the archive file. Shutdown will be delayed. 
* Default: false 

max_mem_usage_mb = <non-negative integer>
* Provides a limitation to the amount of RAM, in megabytes (MB), a batch of 
  events or results will use in the memory of a search process.
* Operates on an estimation of memory use which is not exact.
* The limitation is applied in an unusual way; if the number of results or
  events exceeds maxresults, AND the estimated memory exceeds this limit, the
  data is spilled to disk.
* This means, as a general rule, lower limits will cause a search to use more
  disk I/O and less RAM, and be somewhat slower, but should cause the same
  results to typically come out of the search in the end.
* This limit is applied currently to a number, but not all search processors.
  However, more will likely be added as it proves necessary.
* The number is thus effectively a ceiling on batch size for many components of
  search for all searches run on this system.
* When set to “0”: Specifies that the size is unbounded. Searches might be
  allowed to grow to arbitrary sizes.
* NOTE: 
  * The mvexpand command uses the “max_mem_usage_mb” value in a different way.
    * The mvexpand command has no combined logic with maxresults.
    * If the memory limit is exceeded, output is truncated, not spilled to disk.
  * The 'stats' processor uses the “max_mem_usage_mb” value in the following way.
    * If the estimated memory usage exceeds the specified limit, the results are 
      spilled to disk.
    * If 0 is specified, the results are spilled to the disk when the number of 
      results exceed the “maxresultrows” setting.
* This value is not exact. The estimation can deviate by an order of magnitude
  or so to both the smaller and larger sides.
* Default: 200

min_batch_size_bytes = <integer>
* Specifies the size, in megabytes (MB), of the file/tar after which the 
  file is handled by the batch reader instead of the trailing processor.
* Global parameter, cannot be configured per input.
* NOTE: Configuring this to a very small value could lead to backing up of jobs
  at the tailing processor.
* Default: 20

regex_cpu_profiling = <bool>
* Enable CPU time metrics for RegexProcessor. Output will be in the 
  metrics.log file.
  Entries in metrics.log will appear per_host_regex_cpu, per_source_regex_cpu,
  per_sourcetype_regex_cpu, per_index_regex_cpu.
* Default: false


[searchresults]
* This stanza controls search results for a variety of Splunk search commands.

compression_level = <integer>
* Compression level to use when writing search results to .csv.gz files.
* Default: 1

maxresultrows = <integer>
* Configures the maximum number of events are generated by search commands
  which grow the size of your result set (such as multikv) or that create
  events. Other search commands are explicitly controlled in specific stanzas
  below.
* This limit should not exceed 50000. Setting this limit higher than 50000
  causes instability.
* Default: 50000

tocsv_maxretry = <integer>
* Maximum number of times to retry the atomic write operation.
* When set to “1”: Specifies that there will be no retries.
* Default: 5

tocsv_retryperiod_ms = <integer>
* Period of time to wait before each retry.
* Default: 500

* These setting control logging of error messages to the info.csv file.
  All messages will be logged to the search.log file regardless of 
  these settings.


[search_info]
* This stanza controls logging of messages to the info.csv file.
* Messages logged to the info.csv file are available to REST API clients
  and Splunk Web. Limiting the messages added to info.csv will mean 
  that these messages will not be available in the UI and/or the REST API.

filteredindexes_log_level = [DEBUG|INFO|WARN|ERROR] 
* Log level of messages when search returns no results because
  user has no permissions to search on queried indexes.

infocsv_log_level = [DEBUG|INFO|WARN|ERROR]
* Limits the messages which are added to the info.csv file to the stated 
  level and above.
* For example, if “infocsv_log_level” is WARN, messages of type WARN 
  and higher will be added to the info.csv file.

max_infocsv_messages  = <positive integer>
* If more than max_infocsv_messages log entries are generated, additional
  entries will not be logged in the info.csv file. All entries will still be 
  logged in the search.log file.

show_warn_on_filtered_indexes = <boolean>
* Log warnings if search returns no results because user has 
  no permissions to search on queried indexes.


[subsearch]
* This stanza controls subsearch results.
* NOTE: This stanza DOES NOT control subsearch results when a subsearch is
  called by commands such as join, append, or appendcols.
* Read more about subsearches in the online documentation:
  http://docs.splunk.com/Documentation/Splunk/latest/Search/Aboutsubsearches

maxout = <integer>
* Maximum number of results to return from a subsearch.
* This value cannot be greater than or equal to 10500.
* Default: 10000

maxtime = <integer>
* Maximum number of seconds to run a subsearch before finalizing
* Default: 60

ttl = <integer>
* The time to live (ttl), in seconds, of the cache for the results of a given 
  subsearch.
* Do not set this below 120 seconds.
* See the definition in the [search] stanza under the “TTL” section for more 
  details on how the ttl is computed.
* Default: 300 (5 minutes)


############################################################################
# SEARCH COMMAND
############################################################################
# This section contains the limitation settings for the search command. 
# The settings are organized by type of setting.

[search]    
# The settings under the [search] stanza are organized by type of setting.
             
############################################################################
# Batch search
############################################################################
# This section contains settings for batch search.

allow_batch_mode = <bool>
* Specifies whether or not to allow the use of batch mode which searches 
  in disk based batches in a time insensitive manner.
* In distributed search environments, this setting is used on the search head.
* Default: true

batch_search_max_index_values = <int>
* When using batch mode, this limits the number of event entries read from the
  index file. These entries are small, approximately 72 bytes. However batch
  mode is more efficient when it can read more entries at one time.
* Setting this value to a smaller number can lead to slower search performance.
* A balance needs to be struck between more efficient searching in batch mode
* and running out of memory on the system with concurrently running searches.
* Default: 10000000

batch_search_max_pipeline = <int>
* Controls the number of search pipelines that are 
  launched at the indexer during batch search.
* Increasing the number of search pipelines should help improve search 
  performance, however there will be an increase in thread and memory usage.
* This setting applies only to searches that run on remote indexers.
* Default: 1

batch_search_max_results_aggregator_queue_size = <int>
* Controls the size, in MB,  of the search results queue to which all 
  the search pipelines dump the processed search results.
* Increasing the size can lead to search performance gains. 
  Decreasing the size can reduce search performance. 
* Do not specify zero for this setting.
* Default: 100

batch_search_max_serialized_results_queue_size = <int>
* Controls the size, in MB, of the serialized results queue from which 
  the serialized search results are transmitted.
* Increasing the size can lead to search performance gains. 
  Decreasing the size can reduce search performance. 
* Do not specify zero for this setting.
* Default: 100

NOTE: The following batch search settings control the periodicity of retries
      to search peers in the event of failure (Connection errors, and others). 
      The interval exists between failure and first retry, as well as 
      successive retries in the event of further failures.

batch_retry_min_interval = <int>
* When batch mode attempts to retry the search on a peer that failed, 
  specifies the minimum time, in seconds, to wait to retry the search.
* Default: 5

batch_retry_max_interval = <int>
* When batch mode attempts to retry the search on a peer that failed,
  specifies the maximum time, in seconds, to wait to retry the search. 
* Default: 300 (5 minutes)

batch_retry_scaling = <double>
* After a batch retry attempt fails, uses this scaling factor to increase
  the time to wait before trying the search again.
* The value should be > 1.0.
* Default: 1.5

batch_wait_after_end = <int>
* The amount of time, in seconds, to wait after a search ends to retry to 
  connect with peers where the connection failed or was lost. 
* Batch mode considers the search ended (finished) when all peers, without
  communication failure, have explicitly indicated that they are complete.
  This means that the peers have delivered the complete answer.  
* Default: 900

############################################################################
# Bundles
############################################################################
# This section contains settings for bundles and bundle replication.

load_remote_bundles = <bool>
* On a search peer, allow remote (search head) bundles to be loaded in splunkd.
* Default: false.

replication_file_ttl = <int>
* The time to live (ttl), in seconds, of bundle replication tarballs, 
  for example: *.bundle files.
* Default: 600 (10 minutes)

replication_period_sec  = <int>
* The minimum amount of time, in seconds, between two successive bundle
  replications.
* Default: 60

sync_bundle_replication = [0|1|auto]
* A flag that indicates whether configuration file replication blocks 
  searches or is run asynchronously.
* When set to “auto”: The Splunk software uses asynchronous
  replication only if all of the peers support asynchronous bundle 
  replication.
  Otherwise synchronous replication is used.
* Default: auto

############################################################################
# Concurrency
############################################################################
# This section contains settings for search concurrency limits.

base_max_searches = <int>
* A constant to add to the maximum number of searches, computed as a 
  multiplier of the CPUs.
* Default: 6

max_rt_search_multiplier = <decimal number>
* A number by which the maximum number of historical searches is multiplied
  to determine the maximum number of concurrent real-time searches.
* Note: The maximum number of real-time searches is computed as:
  max_rt_searches = max_rt_search_multiplier x max_hist_searches
* Default: 1

max_searches_per_cpu = <int>
* The maximum number of concurrent historical searches for each CPU. 
  The system-wide limit of historical searches is computed as:
  max_hist_searches =  max_searches_per_cpu x number_of_cpus + base_max_searches
* NOTE: The maximum number of real-time searches is computed as:
  max_rt_searches = max_rt_search_multiplier x max_hist_searches
* Default: 1

############################################################################
# Distributed search
############################################################################
# This section contains settings for distributed search connection 
# information.

addpeer_skew_limit = <positive integer>
* Absolute value of the largest time skew, in seconds, that is allowed when 
  configuring a search peer from a search head, independent of time.
* If the difference in time (skew) between the search head and the peer is 
  greater than “addpeer_skew_limit”, the search peer is not added.
* This is only relevant to manually added peers. This setting has no effect
  on index cluster search peers.
* Default: 600 (10 minutes)

fetch_remote_search_log = [enabled|disabledSavedSearches|disabled]
* When set to “enabled”: All remote search logs are downloaded barring 
  the oneshot search.
* When set to “disabledSavedSearches”: Downloads all remote logs other 
  than saved search logs and oneshot search logs.
* When set to “disabled”: Irrespective of the search type, all remote 
  search log download functionality is disabled.
* NOTE: 
  * The previous values:[true|false] are still supported but not recommended.
  * The previous value of “true” maps to the current value of “enabled”.
  * The previous value of “false” maps to the current value of “disabled”.
* Default: disabledSavedSearches

max_chunk_queue_size = <int>
* The maximum size of the chunk queue.
* default: 10000000

max_combiner_memevents = <int>
* Maximum size of the in-memory buffer for the search results combiner. 
  The <int> is the number of events.
* Default: 50000

max_tolerable_skew = <positive integer>
* Absolute value of the largest timeskew, in seconds, that we will tolerate
  between the native clock on the search head and the native clock on the peer
  (independent of time-zone).
* If this time skew is exceeded, a warning is logged. This estimate is
  approximate and tries to account for network delays.
* Default: 60

max_workers_searchparser = <int>
* The number of worker threads in processing search result when using round
  robin policy.
* default: 5

results_queue_min_size = <integer>
* The minimum size, of search result chunks, that will be kept from peers 
  for processing on the search head before throttling the rate that data
  is accepted.
* The minimum queue size in chunks is the “results_queue_min_size” value 
  and the number of peers providing results, which ever is greater.
* Default: 10

result_queue_max_size = <integer>
* The maximum size, in MB, that will be kept from peers for processing on 
  the search head before throttling the rate that data is accepted.
* The “results_queue_min_size” value takes precedence. The number of search
  results chunks specified by “results_queue_min_size” will always be 
  retained in the queue even if the combined size in MB exceeds the 
  “result_queue_max_size” value. 
* Default: 100

############################################################################
# Field stats 
############################################################################
# This section contains settings for field statistics.

fieldstats_update_freq = <number>
* How often to update the field summary statistics, as a ratio to the elapsed
  run time so far.
* Smaller values means update more frequently. 
* When set to “0”: Specifies to update as frequently as possible.
* Default: 0

fieldstats_update_maxperiod = <number>
* The maximum period, in seconds, for updating field summary statistics.
* When set to “0”: Specifies that there is not maximum period. The period 
  is dictated by the calculation:
  current_run_time x fieldstats_update_freq
* Fractional seconds are allowed.
* Default: 60

min_freq = <number>
* Minimum frequency of a field that is required for the field to be included
  in the /summary endpoint.
* The frequency must be a fraction >=0 and <=1.
* Default: 0.01 (1%)

############################################################################
# History
############################################################################
# This section contains settings for search history.

enable_history = <bool>
* Specifies whether to keep a history of the searches that are run.
* Default: true

max_history_length = <int>
* Maximum number of searches to store in history for each user and application.
* Default: 1000

############################################################################
# Memory tracker
############################################################################
# This section contains settings for the memory tracker.

enable_memory_tracker = <bool>
* Specifies if the memory tracker is enabled.
* When set to “false” (disabled): The search is not terminated even if 
  the search exceeds the memory limit.
* When set to “true”: Enables the memory tracker. 
* Must be set to “true” to enable the “search_process_memory_usage_threshold” 
  setting or the “search_process_memory_usage_percentage_threshold” setting.
* Default: false

search_process_memory_usage_threshold = <double>
* To use this setting, the “enable_memory_tracker” setting must be set 
  to “true”.
* Specifies the maximum memory, in MB, that the search process can consume 
  in RAM.
* Search processes that violate the threshold are terminated.
* If the value is set to 0, then search processes are allowed to grow 
  unbounded in terms of in memory usage.  
* Default: 4000 (4GB)

search_process_memory_usage_percentage_threshold = <float>
* To use this setting, the “enable_memory_tracker” setting must be set
  to “true”.
* Specifies the percent of the total memory that the search process is 
  entitled to consume.
* Search processes that violate the threshold percentage are terminated.
* If the value is set to zero, then splunk search processes are allowed to 
  grow unbounded in terms of percentage memory usage.  
* Any setting larger than 100 or less than 0 is discarded and the default 
  value is used.
* Default: 25%

############################################################################
# Meta search
############################################################################
# This section contains settings for meta search.

allow_inexact_metasearch = <bool>
* Specifies if a metasearch that is inexact be allowed.  
* When set to “true”: An INFO message is added to the inexact metasearches.  
* When set to “false”: A fatal exception occurs at search parsing time.
* Default: false

indexed_as_exact_metasearch = <bool>
* Specifies if a metasearch can process <field>=<value> the same as
  <field>::<value>, if <field> is an indexed field. 
* When set to “true”: Allows a larger set of metasearches when the 
  “allow_inexact_metasearch” setting is “false”. However, some of the 
  metasearches might be inconsistent with the results of doing a normal 
  search.
* Default: false

############################################################################
# Misc 
############################################################################
# This section contains miscellaneous search settings.

disk_usage_update_period = <number>
* Specifies how frequently, in seconds, should the search process estimate the
  artifact disk usage.
* The quota for the amount of disk space that a search job can use is
  controlled by the 'srchDiskQuota' setting in authorize.conf.
* Exceeding this quota causes the search to be auto-finalized immediately,
  even if there are results that have not yet been returned.
* Fractional seconds are allowed.
* Default: 10

dispatch_dir_warning_size = <int>
* Specifies the number of jobs in the dispatch directory that triggers when
  to issue a bulletin message. The message warns that performance might 
  be impacted.
* Default: 5000

do_not_use_summaries = <bool>
* Do not use this setting without working in tandem with Splunk support.
* This setting is a very narrow subset of “summary_mode=none”. 
* When set to “true”: Disables some functionality that is necessary for 
  report acceleration. 
  * In particular, when set to “true”, search processes will no longer query 
    the main splunkd's /admin/summarization endpoint for report acceleration 
     summary IDs.
* In certain narrow use-cases this might improve performance if report 
  acceleration (savedsearches.conf:auto_summarize) is not in use, by lowering 
  the main splunkd's process overhead.
* Default: false

enable_datamodel_meval = <bool>
* Enable concatenation of successively occurring evals into a single
  comma-separated eval during the generation of datamodel searches.
* default: true

force_saved_search_dispatch_as_user = <bool>
* Specifies whether to overwrite the “dispatchAs” value.
* When set to “true”: The “dispatchAs” value is overwritten by “user” 
  regardless of the [user|owner] value in the savedsearches.conf file.
* When set to “false”: The value in the savedsearches.conf file is used.
* You might want to set this to “true” to effectively disable 
  “dispatchAs = owner” for the entire install, if that more closely aligns 
  with security goals.
* Default: false

max_id_length = <integer>
* Maximum length of the custom search job ID when spawned by using
  REST API argument “id”.

search_keepalive_frequency = <int>
* Specifies how often, in milliseconds, a keepalive is sent while a search is running.
* Default: 30000 (30 seconds)

search_keepalive_max = <int>
* The maximum number of uninterupted keepalives before the connection is closed.
* This counter is reset if the search returns results. 
* Default: 100

stack_size = <int>
* The stack size, in bytes, of the thread that executes the search.
* Default: 4194304 (4MB)

summary_mode = [all|only|none]
* Specifies if precomputed summary data are to be used.
* When set to “all”: Use summary data if possible, otherwise use raw data.
* When set to “only”: Use summary data if possible, otherwise do not use 
  any data.
* When set to “none”: Never use precomputed summary data.
* Default: all

track_indextime_range = <bool>
* Specifies if the system should track the _indextime range of returned 
  search results.
* Default: true

use_bloomfilter = <bool>
* Controls whether to use bloom filters to rule out buckets.
* Default: true

use_metadata_elimination = <bool>
* Control whether to use metadata to rule out buckets.
* Default: true

use_dispatchtmp_dir = <bool>
* Specifies if the dispatchtmp directory should be used for temporary search 
  time files, to write temporary files to a different directory from the 
  dispatch directory for the job.
* Temp files are written to $SPLUNK_HOME/var/run/splunk/dispatchtmp/<sid>/ 
  directory.
* In search head pooling, performance can be improved by mounting dispatchtmp 
  to the local file system.
* Default: true, if search head pooling is enabled. Otherwise false.

auto_cancel_after_pause = <integer>
* Specifies the amount of time, in seconds, that a search must be paused before
  the search is automatically cancelled.
* If set to 0, a paused search is never automatically cancelled.
* Default: 0

############################################################################
# Parsing
############################################################################
# This section contains settings related to parsing searches.

max_macro_depth = <int>
* Maximum recursion depth for macros. Specifies the maximum levels for macro 
  expansion.
* It is considered a search exception if macro expansion does not stop after 
  this many levels.
* Value must be greater than or equal to 1.
* Default: 100

max_subsearch_depth = <int>
* Maximum recursion depth for subsearches. Specifies the maximum levels for
  subsearches. 
* It is considered a search exception if a subsearch does not stop after 
  this many levels.
* Default: 8

min_prefix_len = <integer>
* The minimum length of a prefix before a wildcard (*) to use in the query
  to the index.  
* Default: 1

use_directives = <bool>
* Specifies whether a search can take directives and interpret them
  into arguments.
* This is used in conjunction with the search optimizer in order to
  improve search performance.
* Default: true

############################################################################
# Phased execution settings
############################################################################
# This section contains settings for multi-phased execution

phased_execution = <bool>
* This controls whether a search runs in a single phased (current) mode,
  or multi-phased (two or three phased) mode.
* If set to "true": The search can run in multi-phased mode.
* If set to "false": The search can only run in single phased mode.
* If a search needs to run in multi-phased mode, you also need to add noop
  the command as the last command in the search string.
* When you add the noop command, you must specify the "phased_mode"
  argument. The "phased_mode" argument is used to limit the phased execution
  for a particular search.
* The value specified for the phased_mode argument determines the number of 
  phases.
  For example, if phased_mode=2, the search execution uses the 2-phased
  mode. If phased_mode=3, the search execution uses the 3-phased mode, which
  includes shuffling.
  If you specify anything other than 2 or 3 for phased_mode, or if
  phased_execution is set to "false", the search execution uses the single
  phased mode.
* Do not enable this system-level setting to turn on the phased execution of
  Splunk Search without consulting Splunk personnel. The phased execution is
  targeted to improve specific search use cases pertaining to: 
  (1) high cardinality group by keys
  (2) transaction processing
  If not carefully applied, the phased execution can cause certain searches
  to slow down.
* Explicitly set to true for the phased_execution to be operational.
* More related settings in [parallelreduce] stanza.  
* Default: false

############################################################################
# Preview
############################################################################
# This section contains settings for previews.

max_preview_period = <integer>
* The maximum time, in seconds, between previews. 
* Used with the preview interval that is calculated with the 
  “preview_duty_cycle” setting.
* When set to “0”: Specifies unlimited time between previews.
* Default: 0

min_preview_period = <integer>
* The minimum time, in seconds, required between previews. When the calculated 
  interval using “preview_duty_cycle” indicates previews should be run 
  frequently. This setting is used to limit the frequency with which previews 
  run. 
* Default: 1

preview_duty_cycle = <number>
* The maximum time to spend generating previews, as a fraction of the total 
  search time.
* Must be > 0.0 and < 1.0
* Default: 0.25

preview_freq = <timespan> or <ratio>
* Minimum amount of time between results preview updates.
* If specified as a number, between > 0 and  < 1, the minimum time between 
  previews is computed as a ratio of the amount of time that the search 
  has been running, or as a ratio of the length of the time window for 
  real-time windowed searches.
* Default: a ratio of 0.05

############################################################################
# Quota or queued searches
############################################################################
# This section contains settings for quota or queued searches.

default_allow_queue = [0|1]
* Unless otherwise specified by using a REST API argument, specifies if an 
  asynchronous job spawning request should be queued on quota violation. 
  If not, an http error of server too busy is returned.
* Default: 1 (true)

dispatch_quota_retry = <integer>
* The maximum number of times to retry to dispatch a search when the quota has
  been reached.
* Default: 4

dispatch_quota_sleep_ms = <integer>
* The time, in milliseconds, between retrying to dispatch a search when a
  quota is reached.
* Retries the given number of times, with each successive wait 2x longer than
  the previous wait time.
* Default: 100

enable_cumulative_quota = <bool>
* Specifies whether to enforce cumulative role based quotas.
* Default: false

queued_job_check_freq = <number>
* Frequency, in seconds, to check queued jobs to determine if the jobs can 
  be started.
* Fractional seconds are allowed.
* Default: 1.

############################################################################
# Reading chunk controls 
############################################################################
# This section contains settings for reading chunk controls.

chunk_multiplier = <integer>
* A multiplier that the “max_results_perchunk”, “min_results_perchunk”, and 
  “target_time_perchunk” settings are multiplied by for a long running search.
* Default: 5

long_search_threshold = <integer>
* The time, in seconds, until a search is considered "long running".
* Default: 2

max_rawsize_perchunk = <integer>
* The maximum raw size, in bytes, of results for each call to search 
  (in dispatch).
* When set to “0”: Specifies that there is no size limit.
* This setting is not affected by the “chunk_multiplier” setting.
* Default: 100000000 (100MB)

max_results_perchunk = <integer>
* The maximum number of results to emit for each call to the preview data 
  generator.
* Default: 2500

max_results_perchunk = <integer>
* Maximum results for each call to search (in dispatch).
* Must be less than or equal to the “maxresultrows” setting.
* Default: 2500

min_results_perchunk = <integer>
* The minimum results for each call to search (in dispatch).
* Must be less than or equal to the “max_results_perchunk” setting.
* Default: 100

target_time_perchunk = <integer>
* The target duration, in milliseconds, of a particular call to fetch 
  search results.
* Default: 2000 (2 seconds)

############################################################################
# Real-time
############################################################################
# This section contains settings for real-time searches.

check_splunkd_period = <number>
* Amount of time, in seconds, that determines how frequently the search process
  (when running a real-time search) checks whether the parent process
  (splunkd) is running or not.
* Fractional seconds are allowed.
* Default: 60 (1 minute)

realtime_buffer = <int>
* Maximum number of accessible events to keep for real-time searches in
  Splunk Web.
* Acts as circular buffer after this buffer limit is reached.
* Must be greater than or equal to 1.
* Default: 10000

############################################################################
# Remote storage
############################################################################
# This section contains settings for remote storage.

bucket_localize_max_timeout_sec = <int>
* The maximum amount of time, in seconds, to spend localizing a bucket stored 
  in remote storage.
* If the bucket contents (what is required for the search) cannot be localized 
  in that timeframe, the bucket will not be searched. 
* When set to “0”: Specifies an unlimited amount of time.
* This setting is only relevant when using remote storage.
* Default: 300 (5 minutes)

bucket_localize_status_check_period_ms = <int>
* The amount of time, in milliseconds, between consecutive status checks to see
  if the needed bucket contents required by the search have been localized.
* This setting is only relevant when using remote storage.
* The minimum and maximum values are 10 and 60000, respectively.  If the
  specified value falls outside this range, it is effectively set to the
  nearest value within the range.  For example, if you set the value to
  70000, the effective value will be 60000.
* Default: 500 (.5 seconds)

bucket_localize_max_lookahead = <int>
* Specifies the maximum number of buckets the search command localizes
  for look-ahead purposes, in addition to the required bucket. 
* Increasing this value can improve performance, at the cost of additional 
  network/io/disk utilization.
* Valid values are 0-64. Any value larger than 64 will be set to 64. Other
  invalid values will be discarded and the default will be substituted.
* This setting is only relevant when using remote storage.
* Default: 5

bucket_predictor = [consec_not_needed|everything]
* Specifies which bucket file prediction algorithm to use.
* Do not change this unless you know what you are doing.
* Default: consec_not_needed

############################################################################
# Results storage 
############################################################################
# This section contains settings for storing final search results.

max_count = <integer>
* The number of events that can be accessible in any given status bucket 
  (when status_buckets = 0).
* The last accessible event in a call that takes a base and count.
* Note: This value does not reflect the number of events displayed in the 
  UI after the search is evaluated or computed.
* Default: 500000

max_events_per_bucket = <integer>
* For searches with “status_buckets>0”, this setting limits the number of 
  events retrieved for each timeline bucket.
* Default: 1000 in code.

status_buckets = <integer>
* The approximate maximum number buckets to generate and maintain in the
  timeline.
* Default: 0, which means do not generate timeline information

truncate_report = [1|0]
* Specifies whether or not to apply the “max_count” setting to report output.
* Default: 0 (false)

write_multifile_results_out = <bool>
* At the end of the search, if results are in multiple files, write out the
  multiple files to the results_dir directory, under the search results 
  directory.
* This setting speeds up post-processing search, since the results will 
  already be split into appropriate size files.
* Default: true

############################################################################
# Search process
############################################################################
# This section contains settings for search process configurations.

idle_process_cache_search_count = <int>
* The number of searches that the search process must reach, before purging 
  older data from the cache. The purge is performed even if the 
  “idle_process_cache_timeout" has not been reached.
* When a search process is allowed to run more than one search, the search
  process can cache some data between searches.
* When set to a negative value: No purge occurs, no matter how many
  searches are run.
* Has no effect on Windows if “search_process_mode” is not ”auto" 
  or if “max_searches_per_process” is set to 0 or 1.
* Default: 8

idle_process_cache_timeout = <number>
* The amount of time, in seconds, that a search process must be idle before
  the system purges some older data from these caches.
* When a search process is allowed to run more than one search, the search
  process can cache some data between searches.
* When set to a negative value: No purge occurs, no matter on how long the
  search process is idle.
* When set to “0”: Purging always occurs, regardless of whether the process 
  has been idle or not.
* Has no effect on Windows if “search_process_mode” is not "auto" or
  if “max_searches_per_process” is set to 0 or 1.
* Default: 0.5 (seconds)

idle_process_regex_cache_hiwater = <int>
* A threshold for the number of entries in the regex cache. If the regex cache
  grows to larger than this number of entries, the systems attempts to 
  purge some of the older entries.
* When a search process is allowed to run more than one search, the search
  process can cache compiled regex artifacts.
* Normally the "idle_process_cache_search count“ and the 
  “idle_process_cache_timeout” settings will keep the regex cache a 
  reasonable size.  This setting is to prevent the cache from growing 
  extremely large during a single large search.
* When set to a negative value: No purge occurs, not matter how large 
  the cache.
* Has no effect on Windows if “search_process_mode” is not "auto" or
  if “max_searches_per_process” is set to 0 or 1.
* Default: 2500

idle_process_reaper_period = <number>
* The amount of time, in seconds, between checks to determine if there are
  too many idle search processes.
* When a search process is allowed to run more than one search, the system 
  checks if there are too many idle search processes.
* Has no effect on Windows if “search_process_mode” is not "auto" or
  if “max_searches_per_process” is set to 0 or 1.
* Default: 30

launcher_max_idle_checks = <int>
* Specifies the number of idle processes that are inspected before giving up
  and starting a new search process.
* When allowing more than one search to run for each process, the system 
  attempts to find an appropriate idle process to use.
* When set to a negative value: Every eligible idle process is inspected.
* Has no effect on Windows if “search_process_mode” is not "auto" or
  if “max_searches_per_process” is set to 0 or 1.
* Default: 5

launcher_threads = <int>
* The number of server thread to run to manage the search processes.
* Valid only when more than one search is allowed to run for each process.
* Has no effect on Windows if “search_process_mode” is not "auto" or
  if “max_searches_per_process” is set to 0 or 1.
* Default: -1 (a value is selected automatically)

max_old_bundle_idle_time = <number>
* The amount of time, in seconds, that a process bundle must be idle before 
  the process bundle is considered for reaping.
* Used when reaping idle search processes and the process is not configured
  with the most recent configuration bundle.
* When set to a negative value: The idle processes are not reaped sooner 
  than normal if the processes are using an older configuration bundle.
* Has no effect on Windows if “search_process_mode” is not "auto" or
  if “max_searches_per_process” is set to 0 or 1.
* Default: 5

max_searches_per_process = <int>
* On UNIX, specifies the maximum number of searches that each search process
  can run before exiting.
* After a search completes, the search process can wait for another search to
  start and the search process can be reused.
* When set to “0” or “1”: The process is never reused. 
* When set to a negative value: There is no limit to the number of searches
  that a process can run.
* Has no effect on Windows if search_process_mode is not "auto”.
* Default: 500

max_time_per_process = <number>
* Specifies the maximum time, in seconds, that a process can spend running
  searches.
* When a search process is allowed to run more than one search, limits how 
  much time a process can accumulate running searches before the process
  must exit.
* When set to a negative value: There is no limit on the amount of time a
  search process can spend running.
* Has no effect on Windows if “search_process_mode” is not "auto" or
  if “max_searches_per_process” is set to 0 or 1.
* NOTE: A search can run longer than the value set for “max_time_per_process”
  without being terminated. This setting ONLY prevents the process from 
  being used to run additional searches after the maximum time is reached.
* Default: 300 (5 minutes)

process_max_age = <number>
* Specifies the maximum age, in seconds, for a search process.
* When a search process is allowed to run more than one search, a process 
  is not reused if the process is older than the value specified.
* When set to a negative value: There is no limit on the the age of the 
  search process.
* This setting includes the time that the process spends idle, which is 
  different than "max_time_per_process" setting.
* Has no effect on Windows if “search_process_mode” is not "auto" or
  if “max_searches_per_process” is set to 0 or 1.
* NOTE: A search can run longer than the the time set for “process_max_age”
  without being terminated. This setting ONLY prevents that process from
  being used to run more searches after the search completes.
* Default: 7200 (120 minutes or 2 hours)

process_min_age_before_user_change = <number>
* The minimum age, in seconds, of an idle process before using a process
  from a different user.
* When a search process is allowed to run more than one search, the system 
  tries to reuse an idle process that last ran a search by the same Splunk 
  user.
* If no such idle process exists, the system tries to use an idle process 
  from a different user. The idle process from a different user must be 
  idle for at least the value specified for the 
  “process_min_age_before_user_change” setting.
* When set to “0”: Any idle process by any Splunk user can be reused.
* When set to a negative value: Only a search process by same Splunk user 
  can be reused. 
* Has no effect on Windows if “search_process_mode” is not "auto" or
  if “max_searches_per_process” is set to 0 or 1.
* Default: 4

search_process_mode = [auto|traditional|debug <debugging-command> <debugging-args>]
* Controls how search processes are started.
* When set to “traditional”: Each search process is initialized completely 
  from scratch.
* When set to “debug”: When set to a string beginning with "debug", 
  searches are routed through the <debugging-command>, where the user can 
  "plug in" debugging tools.
  * The <debugging-command> must reside in one of the following locations:
    * $SPLUNK_HOME/etc/system/bin/
    * $SPLUNK_HOME/etc/apps/$YOUR_APP/bin/     
    * $SPLUNK_HOME/bin/scripts/
  * The <debugging-args> are passed, followed by the search command it
    would normally run, to <debugging-command>
    * For example, given the following setting:
        search_process_mode = debug $SPLUNK_HOME/bin/scripts/search-debugger.sh 5
      A command similar to the following is run:
        $SPLUNK_HOME/bin/scripts/search-debugger.sh 5 splunkd search --id=... --maxbuckets=... --ttl=... [...]
* Default: auto

############################################################################
# Search reuse
############################################################################
# This section contains settings for search reuse.

allow_reuse = <bool>
* Specifies whether to allow normally executed historical searches to be 
  implicitly re-used for newer requests if the newer request allows it.
* Default: true

reuse_map_maxsize = <int>
* Maximum number of jobs to store in the reuse map.
* Default: 1000

############################################################################
# Splunk Analytics for Hadoop
############################################################################
# This section contains settings for use with Splunk Analytics for Hadoop.

reduce_duty_cycle = <number>
* The maximum time to spend performing the reduce, as a fraction of total 
  search time.
* Must be > 0.0 and < 1.0.
* Default: 0.25

reduce_freq = <integer>
* When the specified number of chunks is reached, attempt to reduce 
  the intermediate results. 
* When set to “0”: Specifies that there is never an attempt to reduce the 
  intermediate result.
* Default: 10

remote_reduce_limit = <unsigned long>
* The number of results processed by a streaming search before a reduce
  is forced.
* NOTE: this option applies only if the search is run with --runReduce=true
  (currently only Splunk Analytics for Hadoop does this)
* When set to “0”: Specifies that there is no limit.
* Default: 1000000

unified_search = <bool>
* Specifies if unified search is turned on for hunk archiving.
* Default: false

############################################################################
# Status
############################################################################
# This section contains settings for search status.

status_cache_size = <int>
* The number of status data for search jobs that splunkd can cache in RAM. 
  This cache improves performance of the jobs endpoint.
* Default: 10000

status_period_ms = <int>
* The minimum amount of time, in milliseconds, between successive
  status/info.csv file updates.
* This setting ensures that search does not spend significant time just 
  updating these files.
  * This is typically important for very large number of search peers.
  * It could also be important for extremely rapid responses from search 
    peers, when the search peers have very little work to do.
* Default: 1000 (1 second)

############################################################################
# Timelines 
############################################################################
# This section contains settings for timelines.

remote_event_download_finalize_pool = <int>
* Size of the pool, in threads, responsible for writing out the full remote events.
* Default: 5

remote_event_download_initialize_pool = <int>
* Size of the pool, in threads, responsible for initiating the remote event fetch.
* Default: 5

remote_event_download_local_pool = <int>
* Size of the pool, in threads, responsible for reading full local events.
* Default: 5

remote_timeline = [0|1]
* Specifies if the timeline can be computed remotely to enable better
  map/reduce scalability.
* Default: 1 (true)

remote_timeline_connection_timeout = <int>
* Connection timeout, in seconds, for fetching events processed by remote 
  peer timeliner.
* Default: 5.

remote_timeline_fetchall = [0|1]
* When set to “1” (true): Splunk fetches all events accessible through the 
  timeline from the remote peers before the job is considered done.
  * Fetching of all events might delay the finalization of some searches, 
    typically those running in verbose mode from the main Search view in 
    Splunk Web.
  * This potential performance impact can be mitigated by lowering the 
    “max_events_per_bucket” settings.
* When set to “0” (false): The search peers might not ship all matching 
  events to the search head, particularly if there is a very large number of them.
   * Skipping the complete fetching of events back to the search head will 
     result in prompt search finalization.
   * Some events may not be available to browse in the UI.
* This setting does NOT affect the accuracy of search results computed by 
  reporting searches.
* Default: 1 (true)

remote_timeline_max_count = <int>
* Maximum number of events to be stored per timeline bucket on each search
  peer.
* Default: 10000

remote_timeline_max_size_mb = <int>
* Maximum size of disk, in MB, that remote timeline events should take 
  on each peer.
* If the limit is reached, a DEBUG message is emitted and should be 
  visible in the job inspector or in messages.
* Default: 100

remote_timeline_min_peers = <int>
* Minimum number of search peers for enabling remote computation of 
  timelines.
* Default: 1 

remote_timeline_parallel_fetch = <bool>
* Specifies whether to connect to multiple peers at the same time when 
  fetching remote events.
* Default: true

remote_timeline_prefetch = <int>
* Specifies the maximum number of full eventuate that each peer should 
  proactively send at the beginning.
* Default: 100

remote_timeline_receive_timeout = <int>
* Receive timeout, in seconds, for fetching events processed by remote peer
  timeliner.
* Default: 10

remote_timeline_send_timeout = <int>
* Send timeout, in seconds, for fetching events processed by remote peer
  timeliner.
* Default: 10

remote_timeline_thread = [0|1]
* Specifies whether to use a separate thread to read the full events from 
  remote peers if “remote_timeline” is used and “remote_timeline_fetchall” 
  is set to “true”. 
  Has no effect if “remote_timeline” or “remote_timeline_fetchall” is set to 
  “false”.
* Default: 1 (true)

remote_timeline_touchperiod = <number>
* How often, in seconds, while a search is running to touch remote timeline 
  artifacts to keep the artifacts from being deleted by the remote peer.
* When set to “0”: The remote timelines are never touched.  
* Fractional seconds are allowed.
* Default: 300 (5 minutes)

timeline_events_preview = <bool>
* When set to “true”: Display events in the Search app as the events are 
  scanned, including events that are in-memory and not yet committed, instead
  of waiting until all of the events are scanned to see the search results.
  You will not be able to expand the event information in the event viewer 
  until events are committed.
* When set to “false”: Events are displayed only after the events are 
  committed (the events are written to the disk).
* This setting might increase disk usage to temporarily save uncommitted 
  events while the search is running. Additionally, search performance might 
  be impacted.
* Default: false

timeline_freq = <timespan> or <ratio>
* The minimum amount of time, in seconds, between timeline commits.
* If specified as a number < 1 (and > 0), minimum time between commits is
  computed as a ratio of the amount of time that the search has been running.
* Default: 0

############################################################################
# TTL
############################################################################
# This section contains time to live (ttl) settings.

cache_ttl = <integer>
* The length of time, in seconds, to persist search cache entries.
* Default: 300 (5 minutes)

default_save_ttl = <integer>
* How long, in seconds, the ttl for a search artifact should be extended in
  response to the save control action.
* When set to 0, the system waits indefinitely.
* Default: 604800 (1 week)

failed_job_ttl = <integer>
* How long, in seconds, the search artifacts should be stored on disk after 
  a job has failed. The ttl is computed relative to the modtime of the 
  status.csv file of the job, if the file exists, or the modtime of the 
  artifact directory for the search job. 
* If a job is being actively viewed in the Splunk UI then the modtime of 
  the status.csv file is constantly updated such that the reaper does not
  remove the job from underneath.
* Default: 86400 (24 hours)

remote_ttl = <integer>
* How long, in seconds, the search artifacts from searches run in behalf of
  a search head should be stored on the indexer after completion.
* Default: 600 (10 minutes)

ttl = <integer>
* How long, in seconds, the search artifacts should be stored on disk after
  the job completes. The ttl is computed relative to the modtime of the 
  status.csv file of the job, if the file exists, or the modtime of the 
  artifact directory for the search job. 
* If a job is being actively viewed in the Splunk UI then the modtime of 
  the status.csv file is constantly updated such that the reaper does not
  remove the job from underneath.
* Default: 600 (10 minutes)

############################################################################
# Unsupported settings 
############################################################################
# This section contains settings that are no longer supported.

enable_status_cache = <bool>
* This is not a user tunable setting.  Do not use this setting without
  working in tandem with Splunk personnel.  This setting is not tested at
  non-default.
* This controls whether the status cache is used, which caches information
  about search jobs (and job artifacts) in memory in main splunkd.
* Normally this cacheing is enabled and assists performance. However, when
  using Search Head Pooling, artifacts in the shared storage location will be
  changed by other search heads, so this cacheing is disabled.
* Explicit requests to jobs endpoints , eg /services/search/jobs/<sid> are
  always satisfied from disk, regardless of this setting.
* Defaults to true; except in Search Head Pooling environments where it
  defaults to false.

status_cache_in_memory_ttl = <positive integer>
* This is not a user tunable setting.  Do not use this setting without working
  in tandem with Splunk personnel. This setting is not tested at non-default.
* This setting has no effect unless search head pooling is enabled, AND
  enable_status_cache has been set to true.
* If set, controls the number of milliseconds which a status cache entry may be
  used before it expires.
* Defaults to 60000, or 60 seconds.

############################################################################
# Unused settings
############################################################################
# This section contains settings that have been deprecated. These settings
# remain listed in this file for backwards compatibility.

max_bucket_bytes = <integer>
* This setting has been deprecated and has no effect.

rr_min_sleep_ms = <int>
* REMOVED.  This setting is no longer used.

rr_max_sleep_ms = <int>
* REMOVED.  This setting is no longer used.

rr_sleep_factor = <int>
* REMOVED.  This setting is no longer used.


############################################################################
# OTHER COMMAND SETTINGS
############################################################################
# This section contains the stanzas for the SPL commands, except for the  
# search command, which is in separate section. 

[anomalousvalue]

maxresultrows = <integer>
* Configures the maximum number of events that can be present in memory at one
  time.
* Default: searchresults::maxresultsrows (which is by default 50000)

maxvalues = <integer>
* Maximum number of distinct values for a field.
* Default: 100000

maxvaluesize = <integer>
* Maximum size, in bytes, of any single value (truncated to this size if 
  larger).
* Default: 1000


[associate]

maxfields = <integer>
* Maximum number of fields to analyze.
* Default: 10000

maxvalues = <integer>
* Maximum number of values for any field to keep track of.
* Default: 10000

maxvaluesize = <integer>
* Maximum length of a single value to consider.
* Default: 1000


[autoregress]

maxp = <integer>
* Maximum number of events for auto regression.
* Default: 10000

maxrange = <integer>
* Maximum magnitude of range for p values when given a range.
* Default: 1000


[concurrency]

batch_search_max_pipeline = <int>
* Controls the number of search pipelines launched at the indexer during 
  batch search.
* Increasing the number of search pipelines should help improve search 
  performance but there will be an increase in thread and memory usage.
* This value applies only to searches that run on remote indexers.
* Default: 1

max_count = <integer>
* Maximum number of detected concurrencies.
* Default: 10000000


[correlate]

maxfields = <integer>
* Maximum number of fields to correlate.
* Default: 1000


[ctable]

* This stanza controls settings for the contingency command. 
* Aliases for the contingency command are: ctable and counttable.

maxvalues = <integer>
* Maximum number of columns/rows to generate (the maximum number of distinct
  values for the row field and column field).
* Default: 1000


[discretize]

* This stanza contains the settings for the bin command.
* Aliases for the bin command are: bucket and discretize.

default_time_bins = <integer>
* When discretizing time for timechart or explicitly via bin, the default bins
  to use if no span or bins is specified.
* Default: 100

maxbins = <integer>
* Maximum number of bins to discretize into.
* If maxbins is not specified or = 0, it defaults to
  searchresults::maxresultrows
* Default: 50000


[findkeywords]

maxevents = <integer>
* Maximum number of events used by the findkeywords command and the 
  Patterns tab.
* Default: 50000


[geomfilter]

enable_clipping = <boolean>
* Whether or not polygons are clipped to the viewport provided by the 
  render client.
* Default: true

enable_generalization = <boolean>
* Whether or not generalization is applied to polygon boundaries to reduce 
  point count for rendering.
* Default: true


[geostats]

filterstrategy = <integer>
* Controls the selection strategy on the geoviz map. 
* Valid values are 1 and 2.

maxzoomlevel = <integer>
* Controls the number of zoom levels that geostats will cluster events on.

zl_0_gridcell_latspan = <float>
* Controls what is the grid spacing in terms of latitude degrees at the 
  lowest zoom level, which is zoom-level 0.
* Grid-spacing at other zoom levels are auto created from this value by 
  reducing by a factor of 2 at each zoom-level.

zl_0_gridcell_longspan = <float>
* Controls what is the grid spacing in terms of longitude degrees at the 
  lowest zoom level, which is zoom-level 0
* Grid-spacing at other zoom levels are auto created from this value by 
  reducing by a factor of 2 at each zoom-level.


[inputcsv]

mkdir_max_retries = <integer>
* Maximum number of retries for creating a tmp directory (with random name as
  subdir of SPLUNK_HOME/var/run/splunk)
* Default: 100


[iplocation]

db_path = <path>
* The absolute path to the GeoIP database in the MMDB format.
* The “db_path” setting does not support standard Splunk environment 
  variables such as SPLUNK_HOME.
* Default: The database that is included with the Splunk platform.


[join]

subsearch_maxout = <integer>
* Maximum result rows in output from subsearch to join against.
* Default: 50000

subsearch_maxtime = <integer>
* Maximum search time, in seconds, before auto-finalization of subsearch.
* Default: 60

subsearch_timeout = <integer>
* Maximum time, in seconds, to wait for subsearch to fully finish.
* Default: 120


[kmeans]

maxdatapoints = <integer>
* Maximum data points to do kmeans clusterings for.
* Default: 100000000 (100 million)

maxkrange = <integer>
* Maximum number of k values to iterate over when specifying a range.
* Default: 100

maxkvalue = <integer>
* Maximum number of clusters to attempt to solve for.
* Default: 1000


[lookup]

batch_index_query = <bool>
* Should non-memory file lookups (files that are too large) use batched queries
  to possibly improve performance?
* Default: true

batch_response_limit = <integer>
* When doing batch requests, the maximum number of matches to retrieve
  if more than this limit of matches would otherwise be retrieve, we will fall
  back to non-batch mode matching
* Default: 5000000

max_lookup_messages = <positive integer>
* If more than "max_lookup_messages" log entries are generated, additional
  entries will not be logged in info.csv. All entries will still be logged in
  search.log.

max_matches = <integer>
* Maximum matches for a lookup.
* Valid values range from 1 - 1000.
* Default: 1000

max_memtable_bytes = <integer>
* Maximum size, in bytes, of static lookup file to use an in-memory index for.
* Lookup files with size above max_memtable_bytes will be indexed on disk
* A large value results in loading large lookup files in memory leading to bigger 
  process memory footprint.
* Caution must be exercised when setting this parameter to arbitrarily high values!
* Default: 10000000 (10MB)

max_reverse_matches = <integer>
* maximum reverse lookup matches (for search expansion)
* Default: 50


[metadata]

bucket_localize_max_lookahead = <int>
* This setting is only relevant when using remote storage.
* Specifies the maximum number of buckets the metadata command localizes
  for look-ahead purposes, in addition to the required bucket. 
* Increasing this value can improve performance, at the cost of additional 
  network/io/disk utilization.
* Valid values are 0-64. Any value larger than 64 will be set to 64. Other
  invalid values will be discarded and the default will be substituted.
* Default: 10

maxcount = <integer>
* The total number of metadata search results returned by the search head;
  after the maxcount is reached, any additional metadata results received from
  the search peers will be ignored (not returned).
* A larger number incurs additional memory usage on the search head.
* Default: 100000

maxresultrows = <integer>
* The maximum number of results in a single chunk fetched by the metadata
  command
* A smaller value will require less memory on the search head in setups with
  large number of peers and many metadata results, though, setting this too
  small will decrease the search performance.
* NOTE: Do not change unless instructed to do so by Splunk Support.
* Default: 10000


[mvexpand]
* This stanza allows for fine tuning of mvexpand search command.

max_mem_usage_mb = <non-negative integer>
* Overrides the default value for “max_mem_usage_mb”.
* Limits the amount of RAM, in megabytes (MB), a batch of events or results will
  use in the memory of a search process.
* See definition in the [default] stanza for “max_mem_usage_mb” for more details.
* Default: 500


[mvcombine]
* This stanza allows for fine tuning of mvcombine search command.

max_mem_usage_mb = <non-negative integer>
* Overrides the default value for “max_mem_usage_mb”
* Limits the amount of RAM, in megabytes (MB), a batch of events or results will
  use in the memory of a search process.
* See definition in the [default] stanza for “max_mem_usage_mb” for more details.
* Default: 500


[outputlookup]

outputlookup_check_permission = <bool>
* Specifies whether the outputlookup command should verify that users 
  have write permissions to CSV lookup table files.
* outputlookup_check_permission is used in conjunction with the 
  transforms.conf setting check_permission. 
* The system only applies outputlookup_check_permission to .csv lookup 
  configurations in transforms.conf that have check_permission=true.
* You can set lookup table file permissions in the .meta file for each lookup 
  file, or through the Lookup Table Files page in Settings. By default, only 
  users who have the admin or power role can write to a shared CSV lookup 
  file.
* Default: false


[rare]

maxresultrows = <integer>
* Maximum number of result rows to create.
* If not specified, defaults to searchresults::maxresultrows
* Default: 50000

maxvalues = <integer>
* Maximum number of distinct field vector values to keep track of.
* Default: 100000

maxvaluesize = <integer>
* Maximum length of a single value to consider.
* Default: 1000


[set]

maxresultrows = <integer>
* The maximum number of results the set command will use from each result 
  set to compute the required set operation.
* Default: 50000


[sort]

maxfiles = <integer>
* Maximum files to open at once.  Multiple passes are made if the number of
  result chunks exceeds this threshold.
* Default: 64.


[spath]

extract_all = <boolean>
* Controls whether we respect automatic field extraction when spath is 
  invoked manually.
* If true, we extract all fields regardless of settings.  If false, we only
  extract fields used by later search commands.
* Default: true

extraction_cutoff = <integer>
* For extract-all spath extraction mode, only apply extraction to the first
  <integer> number of bytes.
* Default: 5000


[stats|sistats]

approx_dc_threshold = <integer>
* When using approximate distinct count (i.e. estdc(<field>) in
  stats/chart/timechart), do not use approximated results if the actual number
  of distinct values is less than this number
* Default: 1000

dc_digest_bits = <integer>
* 2^<integer> bytes will be size of digest used for approximating distinct 
  count.
* Must be >= 8 (128B) and <= 16 (64KB)
* Default: 10 (equivalent to 1KB)

default_partitions = <int>
* Number of partitions to split incoming data into for parallel/multithreaded reduce
* Default: 1

list_maxsize = <int>
* Maximum number of list items to emit when using the list() function
  stats/sistats
* Default: 100

maxmem_check_freq = <integer>
* How frequently, in rows, to check to see if we are exceeding the in 
  memory data structure size limit as specified by “max_mem_usage_mb”.
* Default: 50000

maxresultrows = <integer>
* Maximum number of rows allowed in the process memory.
* When the search process exceeds “max_mem_usage_mb” and “maxresultrows”, 
  data is spilled out to the disk.
* If not specified, defaults to searchresults::maxresultrows
* Default: 50000

max_stream_window = <integer>
* For the streamstats command, the maximum allow window size.
* Default: 10000

maxvalues = <integer>
* Maximum number of values for any field to keep track of.
* When set to “0”: Specifies an unlimited number of values.
* Default: 0

maxvaluesize = <integer>
* Maximum length of a single value to consider.
* When set to “0”: Specifies an unlimited number of values.
* Default: 0 

max_valuemap_bytes = <integer>
* For the sistats command, the maximum encoded length of the valuemap, 
  per result written out.
* If limit is exceeded, extra result rows are written out as needed.  
* 0 = no limit per row
* Default: 100000

natural_sort_output = <bool>
* Do a natural sort on the output of stats if output size is <= maxresultrows
* Natural sort means that we sort numbers numerically and non-numbers
  lexicographically
* Default: true

partitions_limit = <int>
* Maximum number of partitions to split into that can be specified via the
  'partitions' option.
* When exceeded, the number of partitions is reduced to this limit.
* Default: 100

perc_method = nearest-rank|interpolated
* Which method to use for computing percentiles (and medians=50 percentile).
  * nearest-rank picks the number with 0-based rank R =
    floor((percentile/100)*count)
  * interpolated means given F = (percentile/100)*(count-1),
    pick ranks R1 = floor(F) and R2 = ceiling(F).
    Answer = (R2 * (F - R1)) + (R1 * (1 - (F - R1)))
* See wikipedia percentile entries on nearest rank and "alternative methods"
* Default: nearest-rank

perc_digest_type = rdigest|tdigest
* Which digest algorithm to use for computing percentiles 
  ( and medians=50 percentile).
  * rdigest picks the rdigest_k, rdigest_maxnodes and perc_method properties.
  * tdigest picks the tdigest_k and tdigest_max_buffer_size properties.
* Default: rdigest

sparkline_maxsize = <int>
* Maximum number of elements to emit for a sparkline
* Default: The value of the “list_maxsize” setting

sparkline_time_steps = <time-step-string>
* Specify a set of time steps in order of decreasing granularity. Use an 
  integer and one of the following time units to indicate each step.
  * s = seconds
  * m = minutes
  * h = hours
  * d = days
  * month
* A time step from this list is selected based on the <sparkline_maxsize> setting. 
* The lowest <sparkline_time_steps> value that does not exceed the maximum number 
* of bins is used.
* Example:
  * If you have the following configurations:
  * <sparkline_time_steps> = 1s,5s,10s,30s,1m,5m,10m,30m,1h,1d,1month
  * <sparkline_maxsize> = 100
  * The timespan for 7 days of data is 604,800 seconds. 
  * Span = 604,800/<sparkline_maxsize>.
  * If sparkline_maxsize = 100, then 
    span = (604,800 / 100) = 60,480 sec == 1.68 hours.
  * The "1d" time step is used because it is the lowest value that does not exceed 
  * the maximum number of bins.
* Default: 1s,5s,10s,30s,1m,5m,10m,30m,1h,1d,1month


NOTE: The following are rdigest and tdigest settings. 
      rdigest is a data structure used to compute approximate order statistics
      (such as median and percentiles) using sublinear space.

rdigest_k = <integer>
* rdigest compression factor
* Lower values mean more compression
* After compression, number of nodes guaranteed to be greater than or equal to
  11 times k.
* Must be greater than or equal to 2.
* Default: 100

rdigest_maxnodes = <integer>
* Maximum rdigest nodes before automatic compression is triggered.
* When set to “1”: Specifies to automatically configure based on k value.
* Default: 1

tdigest_k = <integer>
* tdigest compression factor
* Higher values mean less compression, more mem usage, but better accuracy.
* Must be greater than or equal to 1.
* Default: 100

tdigest_max_buffer_size = <integer>
* Maximum number of elements before automatic reallocation of buffer storage is triggered.
* Smaller values result in less memory usage but is slower.
* Very small values (<100) are not recommended as they will be very slow.
* Larger values help performance up to a point after which it actually hurts performance.
* Recommended range is around 10tdigest_k to 30tdigest_k.
* Default: 2048


[top]

maxresultrows = <integer>
* Maximum number of result rows to create.
* If not specified, defaults to searchresults::maxresultrows.
* Default: 50000

maxvalues = <integer>
* Maximum number of distinct field vector values to keep track of.
* Default: 100000

maxvaluesize = <integer>
* Maximum length of a single value to consider.
* Default: 1000


[transactions]

maxopentxn = <integer>
* Specifies the maximum number of not yet closed transactions to keep in the
  open pool before starting to evict transactions.
* Default: 5000

maxopenevents = <integer>
* Specifies the maximum number of events (which are) part of open transactions
  before transaction eviction starts happening, using LRU policy.
* Default: 100000


[tscollect]

squashcase = <boolean>
* The default value of the 'squashcase' argument if not specified by the command
* Default: false

keepresults = <boolean>
* The default value of the 'keepresults' argument if not specified by the command
* Default: false

optimize_max_size_mb = <unsigned int>
* The maximum size in megabytes of files to create with optimize
* Specify 0 for no limit (may create very large tsidx files)
* Default: 1024


[tstats]

allow_old_summaries = <boolean>
* The default value of 'allow_old_summaries' arg if not specified by the
  command
* When running tstats on an accelerated datamodel, allow_old_summaries=false
  ensures we check that the datamodel search in each bucket's summary metadata
  is considered up to date with the current datamodel search. Only summaries
  that are considered up to date will be used to deliver results.
* The allow_old_summaries=true attribute overrides this behavior and will deliver results
  even from bucket summaries that are considered out of date with the current
  datamodel.
* Default: false

apply_search_filter = <boolean>
* Controls whether we apply role-based search filters when users run tstats on
  normal index data
* Note: we never apply search filters to data collected with tscollect or 
  datamodel acceleration
* Default: true

chunk_size = <unsigned int>
* ADVANCED: The default value of 'chunk_size' arg if not specified by 
  the command
* This argument controls how many events are retrieved at a time within a
  single TSIDX file when answering queries
* Consider lowering this value if tstats queries are using too much memory
  (cannot be set lower than 10000)
* Larger values will tend to cause more memory to be used (per search) and
  might have performance benefits.
* Smaller values will tend to reduce performance and might reduce memory used
  (per search).
* Altering this value without careful measurement is not advised.
* Default: 10000000

summariesonly = <boolean>
* The default value of 'summariesonly' arg if not specified by the command
* When running tstats on an accelerated datamodel, summariesonly=false implies
  a mixed mode where we will fall back to search for missing TSIDX data
* summariesonly=true overrides this mixed mode to only generate results from
  TSIDX data, which may be incomplete
* Default: false

warn_on_missing_summaries = <boolean>
* ADVANCED: Only meant for debugging summariesonly=true searches on 
  accelerated datamodels.
* When true, search will issue a warning for a tstats summariesonly=true 
  search for the following scenarios:
    a) If there is a non-hot bucket that has no corresponding datamodel 
    acceleration summary whatsoever.
    b) If the bucket's summary does not match with the current datamodel 
    acceleration search.
* Default: false


[typeahead]

cache_ttl_sec = <integer>
* How long, in seconds, the typeahead cached results are valid.
* Default 300

fetch_multiplier = <integer>
* A multiplying factor that determines the number of terms to fetch from the
  index, fetch = fetch_multiplier x count.
* Default: 50

max_concurrent_per_user = <integer>
* The maximum number of concurrent typeahead searches per user. Once this
  maximum is reached only cached typeahead results might be available
* Default: 3

maxcount = <integer>
* Maximum number of typeahead results to find.
* Default: 1000

min_prefix_length = <integer>
* The minimum length of the string prefix after which to provide typeahead.
* Default: 1

use_cache = [0|1]
* Specifies whether the typeahead cache will be used if use_cache is not
  specified in the command line or endpoint.
* Default: true or 1


[typer]

maxlen = <int>
* In eventtyping, pay attention to first <int> characters of any attribute
  (such as _raw), including individual tokens. Can be overridden by supplying
  the typer operator with the argument maxlen (for example,
  "|typer maxlen=300").
* Default: 10000


[xyseries]

* This stanza allows for fine tuning of xyseries search command.

max_mem_usage_mb = <non-negative integer>
* Overrides the default value for “max_mem_usage_mb”
* See definition in [default] max_mem_usage_mb for more details



############################################################################
# GENERAL SETTINGS
############################################################################
# This section contains the stanzas for a variety of general settings. 


[authtokens]

expiration_time = <integer>
* Expiration time, in seconds, of auth tokens.
* Default: 3600 (60 minutes)


[auto_summarizer]

allow_event_summarization = <bool>
* Whether auto summarization of searches whose remote part returns events
  rather than results will be allowed.
* Default: false

cache_timeout = <integer>
* The amount of time, in seconds, to cache auto summary details and search hash
  codes
* Default: 600 (10 minutes)

detailed_dashboard = <bool>
* Turn on/off the display of both normalized and regular summaries in the
  Report Acceleration summary dashboard and details.
* Default: false

maintenance_period = <integer>
* The period of time, in seconds, that the auto summarization maintenance
  happens
* Default: 1800 (30 minutes)

max_run_stats = <int>
* Maximum number of summarization run statistics to keep track and expose via
  REST.
* Default: 48

max_verify_buckets = <int>
* When verifying buckets, stop after verifying this many buckets if no failures
  have been found
* 0 means never
* Default: 100

max_verify_bucket_time = <int>
* Maximum time, in seconds, to spend verifying each bucket.
* Default: 15

max_verify_ratio = <number>
* Maximum fraction of data in each bucket to verify
* Default: 0.1 (10%)

max_verify_total_time = <int>
* Maximum total time in seconds to spend doing verification, regardless if any
  buckets have failed or not
* When set to “0”: Specifies no limit.
* Default: 0

normalized_summaries = <bool>
* Turn on/off normalization of report acceleration summaries.
* Default: true 

return_actions_with_normalized_ids = [yes|no|fromcontext]
* Report acceleration summaries are stored under a signature/hash which can be
  regular or normalized.
  * Normalization improves the re-use of pre-built summaries but is not
    supported before 5.0. This config will determine the default value of how
    normalization works (regular/normalized)
  * When set to ”fromcontext”: Specifies that the end points and summaries 
    would be operating based on context.
* Normalization strategy can also be changed via admin/summarization REST calls
  with the "use_normalization"  parameter which can take the values
  "yes"/"no"/"fromcontext"
* Default: fromcontext

search_2_hash_cache_timeout = <integer>
* The amount of time, in seconds, to cache search hash codes
* Default: The value of the “cache_timeout” setting, which by default is 600 (10 minutes)

shc_accurate_access_counts = <bool>
* Only relevant if you are using search head clustering
* Turn on/off to make acceleration summary access counts accurate on the
  captain.
* by centralizing 

verify_delete = <bool>
* Should summaries that fail verification be automatically deleted?
* Default: false


[export]

add_offset = <bool>
* Add an offset/row number to JSON streaming output
* Default: true

add_timestamp = <bool>
* Add a epoch time timestamp to JSON streaming output that reflects the time
  the results were generated/retrieved
* Default: false


[extern]

perf_warn_limit = <integer>
* Warn when external scripted command is applied to more than this many 
  events
* When set to “0”: Specifies for no message (message is always INFO level)
* Default: 10000


[http_input]

max_number_of_tokens = <unsigned int>
* The maximum number of tokens reported by logging input metrics.
* Default: 10000

max_content_length = <integer>
* The maximum length of http request content accepted by HTTP Input server.
* Default: 1000000 (~ 1MB)

max_number_of_ack_channel = <integer>
* The maximum number of ACK channels accepted by HTTP Event Collector 
  server.
* Default: 1000000 (~ 1 million)

max_number_of_acked_requests_pending_query = <integer>
* The maximum number of ACKed requests pending query on HTTP Event 
  Collector server.
* Default: 10000000 (~ 10 million)

max_number_of_acked_requests_pending_query_per_ack_channel = <integer>
* The maximum number of ACKed requested pending query per ACK channel on HTTP
  Event Collector server..
* Default: 1000000 (~ 1 million)

metrics_report_interval = <integer>
* The interval, in seconds, of logging input metrics report.
* Default: 60 (1 minute)


[indexpreview]

max_preview_bytes = <integer>
* Maximum number of bytes to read from each file during preview
* Default: 2000000 (2 MB)

max_results_perchunk = <integer>
* Maximum number of results to emit per call to preview data generator
* Default: 2500

soft_preview_queue_size = <integer>
* Loosely-applied maximum on number of preview data objects held in memory
* Default: 100


[inputproc]

file_tracking_db_threshold_mb = <integer>
* This setting controls the trigger point at which the file tracking db (also
  commonly known as the "fishbucket" or btree) rolls over.  A new database is
  created in its place.  Writes are targeted at new db.  Reads are first
  targeted at new db, and we fall back to old db for read failures.  Any reads
  served from old db successfully will be written back into new db.
* MIGRATION NOTE: if this setting doesn't exist, the initialization code in
  splunkd triggers an automatic migration step that reads in the current value
  for "maxDataSize" under the "_thefishbucket" stanza in indexes.conf and
  writes this value into etc/system/local/limits.conf.

learned_sourcetypes_limit = <0 or positive integer>
* Limits the number of entries added to the learned app for performance
  reasons.
* If nonzero, limits two properties of data added to the learned app by the
  file classifier. (Code specific to monitor:: stanzas that auto-determines
  sourcetypes from content.)
  * The number of sourcetypes added to the learned app's props.conf file will
    be limited to approximately this number.
  * The number of file-content fingerprints added to the learned app's
    sourcetypes.conf file will be limited to approximately this number.
* The tracking for uncompressed and compressed files is done separately, so in
  some cases this value may be exceeded.
* This limit is not the recommended solution for auto-identifying sourcetypes.
  The usual  best practices are to set sourcetypes in input stanzas, or
  alternatively to apply them based on filename pattern in props.conf
  [source::<pattern>] stanzas.
* Default: 1000

max_fd = <integer>
* Maximum number of file descriptors that a ingestion pipeline in Splunk 
  will keep open, to capture any trailing data from files that are written 
  to very slowly.
* Note that this limit will be applied per ingestion pipeline. For more 
  information about multiple ingestion pipelines see parallelIngestionPipelines
  in the server.conf.spec file.
* With N parallel ingestion pipelines the maximum number of file descriptors that
  can be open across all of the ingestion pipelines will be N * max_fd.
* Default: 100

monitornohandle_max_heap_mb = <integer>
* Controls the maximum memory used by the Windows-specific modular input
  MonitorNoHandle.
* The memory of this input grows in size when the data being produced
  by applications writing to monitored files comes in faster than the Splunk
  system can accept it.
* When set to 0, the heap size (memory allocated in the modular input) can grow
  without limit.
* If this size is limited, and the limit is encountered, the input will drop
  some data to stay within the limit.
* Default: 0

tailing_proc_speed = <integer>
* REMOVED.  This setting is no longer used.

time_before_close = <integer>
* MOVED.  This setting is now configured per-input in inputs.conf.
* Specifying this setting in limits.conf is DEPRECATED, but for now will
  override the setting for all monitor inputs.


[journal_compression]

threads = <integer>
* Specifies the maximum number of indexer threads which will be work on
  compressing hot bucket journal data.
* This setting does not typically need to be modified.
* Default: The number of CPU threads of the host machine


[kv]

avg_extractor_time = <integer>
* Maximum amount of CPU time, in milliseconds, that the average (over search
  results) execution time of a key-value pair extractor will be allowed to take
  before warning. Once the average becomes larger than this amount of time a
  warning will be issued
* Default: 500 (.5 seconds)

limit = <integer>
* The maximum number of fields that an automatic key-value field extraction
  (auto kv) can generate at search time.
* If search-time field extractions are disabled (KV_MODE=none in props.conf)
  then this setting determines the number of index-time fields that will be
  returned.
* The summary fields 'host', 'index', 'source', 'sourcetype', 'eventtype',
  'linecount', 'splunk_server', and 'splunk_server_group' do not count against
  this limit and will always be returned.
* Increase this setting if, for example, you have indexed data with a large
  number of columns and want to ensure that searches display all fields from
  the data.
* Default: 100

maxchars = <integer>
* Truncate _raw to this size and then do auto KV.
* Default: 10240 characters

maxcols = <integer>
* When non-zero, the point at which kv should stop creating new fields.
* Default: 512

max_extractor_time = <integer>
* Maximum amount of CPU time, in milliseconds, that a key-value pair extractor
  will be allowed to take before warning. If the extractor exceeds this
  execution time on any event a warning will be issued
* Default: 1000 (1 second)


[kvstore]

max_accelerations_per_collection = <unsigned int>
* The maximum number of accelerations that can be assigned to a single
  collection
* Valid values range from 0 to 50
* Default: 10

max_documents_per_batch_save = <unsigned int>
* The maximum number of documents that can be saved in a single batch
* Default: 1000

max_fields_per_acceleration = <unsigned int>
* The maximum number of fields that can be part of a compound acceleration
  (i.e. an acceleration with multiple keys)
* Valid values range from 0 to 50
* Default: 10

max_queries_per_batch = <unsigned int>
* The maximum number of queries that can be run in a single batch
* Default: 1000

max_rows_in_memory_per_dump = <unsigned int>
* The maximum number of rows in memory before flushing it to the CSV projection
  of KVStore collection.
* Default: 200

max_rows_per_query = <unsigned int>
* The maximum number of rows that will be returned for a single query to 
  a collection.
* If the query returns more rows than the specified value, then returned 
  result set will contain the number of rows specified in this value.
* Default: 50000

max_size_per_batch_result_mb = <unsigned int>
* The maximum size, in megabytes (MB), of the result set from a set of 
  batched queries
* Default: 100

max_size_per_batch_save_mb = <unsigned int>
* The maximum size, in megabytes (MB), of a batch save query.
* Default: 50

max_size_per_result_mb = <unsigned int>
* The maximum size, in megabytes (MB), of the result that will be 
  returned for a single query to a collection.
* Default: 50

max_threads_per_outputlookup = <unsigned int>
* The maximum number of threads to use during outputlookup commands on KVStore
* If the value is 0 the thread count will be determined by CPU count
* Default: 1


[ldap]

allow_multiple_matching_users = <bool>
* This controls whether we allow login when we find multiple entries with the
  same value for the username attribute
* When multiple entries are found, we choose the first user DN
  lexicographically
* Setting this to false is more secure as it does not allow any ambiguous
  login, but users with duplicate entries will not be able to login.
* Default: true

max_users_to_precache = <unsigned integer>
* The maximum number of users we will attempt to pre-cache from LDAP after 
  reloading auth
* Set this to 0 to turn off pre-caching


[metrics]

interval = <integer>
* Number of seconds between logging splunkd metrics to metrics.log.
* Minimum of 10.
* Default: 30

maxseries = <integer>
* The number of series to include in the per_x_thruput reports in metrics.log.
* Default: 10


[metrics:tcpin_connections]

aggregate_metrics = [true|false]
* For each splunktcp connection from forwarder, splunk logs metrics information
  every metrics interval.
* When there are large number of forwarders connected to indexer, the amount of
  information logged can take lot of space in metrics.log. When set to true, it
  will aggregate information across each connection and report only once per
  metrics interval.
* Default: false

suppress_derived_info = [true|false]
* For each forwarder connection, _tcp_Bps, _tcp_KBps, _tcp_avg_thruput,
  _tcp_Kprocessed is logged in metrics.log.
* This can be derived from kb. When set to true, the above derived info will
  not be emitted.
* Default: false


[pdf]

max_rows_per_table = <unsigned int>
* The maximum number of rows that will be rendered for a table within
  integrated PDF rendering
* Default: 1000

render_endpoint_timeout = <unsigned int>
* The number of seconds after which the pdfgen render endpoint will timeout if
  it has not yet finished rendering the PDF output
* Default: 3600 (60 minutes)


[realtime]

# Default options for indexer support of real-time searches
# These can all be overridden for a single search via REST API arguments

alerting_period_ms = <int>
* This limits the frequency that we will trigger alerts during a realtime search
* A value of 0 means unlimited and we will trigger an alert for every batch of
  events we read in dense realtime searches with expensive alerts this can
  overwhelm the alerting system.
* Precedence: Searchhead
* Default: 0

blocking = [0|1]
* Specifies whether the indexer should block if a queue is full.
* Default: false

default_backfill = <bool>
* Specifies if windowed real-time searches should backfill events
* Default: true

enforce_time_order = <bool>
* Specifies if real-time searches should ensure that events are sorted in
  ascending time order (the UI will automatically reverse the order that it
  display events for real-time searches so in effect the latest events will be
  first)
* Default: true

indexfilter = [0|1]
* Specifies whether the indexer should prefilter events for efficiency.
* Default: 1 (true)

indexed_realtime_update_interval = <int>
* When you run an indexed realtime search, the list of searchable buckets
  needs to be updated. If the Splunk software is installed on a cluster,
  the list of allowed primary buckets is refreshed. If not installed on
  a cluster, the list of buckets, including any new hot buckets are refreshed.
  This setting controls the interval for the refresh. The setting must be
  less than the "indexed_realtime_disk_sync_delay" setting. If your realtime
  buckets transition from new to warm in less time than the value specified
  for the "indexed_realtime_update_interval" setting, data will be skipped
  by the realtime search in a clustered environment.
* Precedence: Indexers
* Default: 30

indexed_realtime_cluster_update_interval = <int>
* This setting is deprecated. Use the "indexed_realtime_update_interval"
  setting instead.
* While running an indexed realtime search, if we are on a cluster we need to
  update the list of allowed primary buckets. This controls the interval that
  we do this. And it must be less than the indexed_realtime_disk_sync_delay. If
  your buckets transition from Brand New to warm in less than this time indexed
  realtime will lose data in a clustered environment.
* Precedence: Indexers
* Default: 30

indexed_realtime_default_span = <int>
* An indexed realtime search is made up of many component historical searches
  that by default will span this many seconds. If a component search is not
  completed in this many seconds the next historical search will span the extra
  seconds. To reduce the overhead of running an indexed realtime search you can
  change this span to delay longer before starting the next component
  historical search.
* Precedence: Indexers
* Default: 1

indexed_realtime_disk_sync_delay = <int>
* This settings controls the number of seconds to wait for disk flushes to
  finish when using indexed/continuous/pseudo realtime search so that we see
  all of the data.
* After indexing there is a non-deterministic period where the files on disk
  when opened by other programs might not reflect the latest flush to disk,
  particularly when a system is under heavy load.
* Precedence: SearchHead overrides Indexers
* Default: 60

indexed_realtime_maximum_span = <int>
* While running an indexed realtime search, if the component searches regularly
  take longer than indexed_realtime_default_span seconds, then indexed realtime
  search can fall more than indexed_realtime_disk_sync_delay seconds behind
  realtime. Use this setting to set a limit after which we will drop data to
  return back to catch back up to the specified delay from realtime, and only
  search the default span of seconds.
* Precedence: API overrides SearchHead overrides Indexers
* Default: 0 (unlimited)

indexed_realtime_use_by_default = <bool>
* Should we use the indexedRealtime mode by default
* Precedence: SearchHead
* Default: false

local_connect_timeout = <int>
* Connection timeout, in seconds, for an indexer's search process when 
  connecting to that indexer's splunkd.
* Default: 5

local_receive_timeout = <int>
* Receive timeout, in seconds, for an indexer's search process when 
  connecting to that indexer's splunkd.
* Default: 5

local_send_timeout = <int>
* Send timeout, in seconds, for an indexer's search process when connecting 
  to that indexer's splunkd.
* Default: 5

max_blocking_secs = <int>
* Maximum time, in seconds, to block if the queue is full (meaningless 
  if blocking = false)
* 0 means no limit
* Default: 60

queue_size = <int>
* Size of queue for each real-time search (must be >0).
* Default: 10000


[restapi]

maxresultrows = <integer>
* Maximum result rows to be returned by /events or /results getters from REST
  API.
* Default: 50000

jobscontentmaxcount = <integer>
* Maximum length of a property in the contents dictionary of an entry from
  /jobs getter from REST API
* Value of 0 disables truncation
* Default: 0

time_format_reject = <regular expression>
* HTTP parameters for time_format and output_time_format which match
  this regex will be rejected (blacklisted).
* The regex will be satisfied by a substring match anywhere in the parameter.
* Intended as defense-in-depth against XSS style attacks against browser users
  by crafting specially encoded URLS for them to access splunkd.
* If unset, all parameter strings will be accepted.
* To disable this check entirely, set the value to empty.
  * Example of disabling: time_format_reject =
* Default: [<>!] , which means that the less-than '<', greater-than '>', and
  exclamation point '!' are not allowed.


[reversedns]

rdnsMaxDutyCycle = <integer>
* Generate diagnostic WARN in splunkd.log if reverse dns lookups are taking
  more than this percent of time
* Range 0-100
* Default: 10


[sample]

maxsamples = <integer>
* Default: 10000

maxtotalsamples = <integer>
* Default: 100000


[scheduler]

action_execution_threads = <integer>
* Number of threads to use to execute alert actions, change this number if your
  alert actions take a long time to execute.
* This number is capped at 10.
* Default: 2

actions_queue_size = <integer>
* The number of alert notifications to queue before the scheduler starts
  blocking, set to 0 for infinite size.
* Default: 100

actions_queue_timeout = <integer>
* The maximum amount of time, in seconds, to block when the action queue size is
  full.
* Default: 30

alerts_expire_period = <integer>
* The amount of time, in seconds, between expired alert removal
* This period controls how frequently the alerts list is scanned, the only
  benefit from reducing this is better resolution in the number of alerts fired
  at the savedsearch level.
* Change not recommended.
* Default: 120

alerts_max_count = <integer>
* Maximum number of unexpired alerts information to keep for the alerts
  manager, when this number is reached Splunk will start discarding the oldest
  alerts.
* Default: 50000

alerts_max_history = <integer>[s|m|h|d]
* Maximum time to search in the past for previously triggered alerts.
* splunkd uses this property to populate the Activity -> Triggered Alerts 
  page at startup.
* Values greater than the default may cause slowdown.
* Relevant units are: s, sec, second, secs, seconds, m, min, minute, mins,
  minutes, h, hr, hour, hrs, hours, d, day, days.
* Default: 7d

alerts_scoping = host|splunk_server|all
* Determines the scoping to use on the search to populate the triggered alerts
  page. Choosing splunk_server will result in the search query
  using splunk_server=local, host will result in the search query using
  host=<search-head-host-name>, and all will have no scoping added to the
  search query.
* Default: splunk_server

auto_summary_perc = <integer>
* The maximum number of concurrent searches to be allocated for auto
  summarization, as a percentage of the concurrent searches that the scheduler
  can run.
* Auto summary searches include:
  * Searches which generate the data for the Report Acceleration feature.
  * Searches which generate the data for Data Model acceleration.
* Note: user scheduled searches take precedence over auto summary searches.
* Default: 50

auto_summary_perc.<n> = <integer>
auto_summary_perc.<n>.when = <cron string>
* The same as auto_summary_perc but the value is applied only when the cron
  string matches the current time.  This allows auto_summary_perc to have
  different values at different times of day, week, month, etc.
* There may be any number of non-negative <n> that progress from least specific
  to most specific with increasing <n>.
* The scheduler looks in reverse-<n> order looking for the first match.
* If either these settings aren't provided at all or no "when" matches the
  current time, the value falls back to the non-<n> value of auto_summary_perc.

concurrency_message_throttle_time = <int>[s|m|h|d]
* Amount of time controlling throttling between messages warning about scheduler 
  concurrency limits.
* Relevant units are: s, sec, second, secs, seconds, m, min, minute, mins,
  minutes, h, hr, hour, hrs, hours, d, day, days.
* Default: 10m 

introspection_lookback = <duration-specifier>
* The amount of time to "look back" when reporting introspection statistics.
* For example: what is the number of dispatched searches in the last 60 minutes?
* Use [<int>]<unit> to specify a duration; a missing <int> defaults to 1.
* Relevant units are: m, min, minute, mins, minutes, h, hr, hour, hrs, hours,
  d, day, days, w, week, weeks.
* For example: "5m" = 5 minutes, "1h" = 1 hour.
* Default: 1h

max_action_results = <integer>
* The maximum number of results to load when triggering an alert action.
* Default: 50000

max_continuous_scheduled_search_lookback = <duration-specifier>
* The maximum amount of time to run missed continuous scheduled searches for
  once Splunk comes back up in the event it was down.
* Use [<int>]<unit> to specify a duration; a missing <int> defaults to 1.
* Relevant units are: m, min, minute, mins, minutes, h, hr, hour, hrs, hours,
  d, day, days, w, week, weeks, mon, month, months.
* For example: "5m" = 5 minutes, "1h" = 1 hour.
* A value of 0 means no lookback.
* Default: 24h

max_lock_files = <int>
* The number of most recent lock files to keep around.
* This setting only applies in search head pooling.

max_lock_file_ttl = <int>
* Time, in seconds, that must pass before reaping a stale lock file.
* Only applies in search head pooling.

max_per_result_alerts = <int>
* Maximum number of alerts to trigger for each saved search instance (or
  real-time results preview for RT alerts)
* Only applies in non-digest mode alerting. Use 0 to disable this limit
* Default: 500

max_per_result_alerts_time = <integer>
* Maximum number of time, in seconds, to spend triggering alerts for each saved search
  instance (or real-time results preview for RT alerts)
* Only applies in non-digest mode alerting. Use 0 to disable this limit.
* Default: 300 (5 minutes)

max_searches_perc = <integer>
* The maximum number of searches the scheduler can run, as a percentage of the
  maximum number of concurrent searches, see [search] max_searches_per_cpu for
  how to set the system wide maximum number of searches.
* Default: 50

max_searches_perc.<n> = <integer>
max_searches_perc.<n>.when = <cron string>
* The same as max_searches_perc but the value is applied only when the cron
  string matches the current time.  This allows max_searches_perc to have
  different values at different times of day, week, month, etc.
* There may be any number of non-negative <n> that progress from least specific
  to most specific with increasing <n>.
* The scheduler looks in reverse-<n> order looking for the first match.
* If either these settings aren't provided at all or no "when" matches the
  current time, the value falls back to the non-<n> value of max_searches_perc.

persistance_period = <integer>
* The period, in seconds, between scheduler state persistance to disk. The
  scheduler currently persists the suppression and fired-unexpired alerts to
  disk.
* This is relevant only in search head pooling mode.
* Default: 30

priority_runtime_factor = <double>
* The amount to scale the priority runtime adjustment by.
* Every search's priority is made higher (worse) by its typical running time.
  Since many searches run in fractions of a second and the priority is
  integral, adjusting by a raw runtime wouldn't change the result; therefore,
  it's scaled by this value.
* Default: 10

priority_skipped_factor = <double>
* The amount to scale the skipped adjustment by.
* A potential issue with the priority_runtime_factor is that now longer-running
  searches may get starved.  To balance this out, make a search's priority
  lower (better) the more times it's been skipped.  Eventually, this adjustment
  will outweigh any worse priority due to a long runtime. This value controls
  how quickly this happens.
* Default: 1

saved_searches_disabled = <bool>
* Whether saved search jobs are disabled by the scheduler.
* Default: false

scheduled_view_timeout = <int>[s|m|h|d]
* The maximum amount of time that a scheduled view (pdf delivery) would be
  allowed to render
* Relevant units are: s, sec, second, secs, seconds, m, min, minute, mins,
  minutes, h, hr, hour, hrs, hours, d, day, days.
* Default: 60m

shc_role_quota_enforcement = <bool>
* When this attribute is enabled, the search head cluster captain enforces
  user-role quotas for scheduled searches globally (cluster-wide).
* A given role can have (n *number_of_members) searches running cluster-wide,
  where n is the quota for that role as defined by srchJobsQuota and
  rtSrchJobsQuota on the captain and number_of_members include the members 
  capable of running scheduled searches.
* Scheduled searches will therefore not have an enforcement of user role 
  quota on a per-member basis.
* Role-based disk quota checks (srchDiskQuota in authorize.conf) can be 
  enforced only on a per-member basis.
  These checks are skipped when shc_role_quota_enforcement is enabled.
* Quota information is conveyed from the members to the captain. Network delays
  can cause the quota calculation on the captain to vary from the actual values
  in the members and may cause search limit warnings. This should clear up as
  the information is synced.
* Default: false

shc_syswide_quota_enforcement = <bool>
* When this is enabled, Maximum number of concurrent searches is enforced
  globally (cluster-wide) by the captain for scheduled searches.
  Concurrent searches include both scheduled searches and ad hoc searches.
* This is (n * number_of_members) where n is the max concurrent searches per node
  (see max_searches_per_cpu for a description of how this is computed) and
  number_of_members include members capable of running scheduled searches.
* Scheduled searches will therefore not have an enforcement of instance-wide
  concurrent search quota on a per-member basis.
* Note that this does not control the enforcement of the scheduler quota.
  For a search head cluster, that is defined as 
  (max_searches_perc * number_of_members)
  and is always enforced globally on the captain.
* Quota information is conveyed from the members to the captain. Network delays
  can cause the quota calculation on the captain to vary from the actual values
  in the members and may cause search limit warnings. This should clear up as
  the information is synced.
* Default: false

shc_local_quota_check = <bool>
* DEPRECATED. Local (per-member) quota check is enforced by default.
* To disable per-member quota checking, enable one of the cluster-wide quota
  checks (shc_role_quota_enforcement or shc_syswide_quota_enforcement).
* For example, setting shc_role_quota_enforcement=true turns off local role
  quota enforcement for all nodes in the cluster and is enforced cluster-wide
  by the captain.

shp_dispatch_to_slave = <bool>
* By default the scheduler should distribute jobs throughout the pool.
* Default: true

search_history_load_timeout = <duration-specifier>
* The maximum amount of time to defer running continuous scheduled searches
  while waiting for the KV Store to come up in order to load historical data.
  This is used to prevent gaps in continuous scheduled searches when splunkd
  was down.
* Use [<int>]<unit> to specify a duration; a missing <int> defaults to 1.
* Relevant units are: s, sec, second, secs, seconds, m, min, minute, mins,
  minutes.
* For example: "60s" = 60 seconds, "5m" = 5 minutes.
* Default: 2m

search_history_max_runtimes = <unsigned int>
* The number of runtimes kept for each search.
* Used to calculate historical typical runtime during search prioritization.
* Default: 10


[search_metrics]

debug_metrics = <bool>
* This indicates whether we should output more detailed search metrics for
  debugging.
* This will do things like break out where the time was spent by peer, and may
  add additional deeper levels of metrics.
* This is NOT related to "metrics.log" but to the "Execution Costs" and
  "Performance" fields in the Search inspector, or the count_map in the 
  info.csv file.
* Default: false


[show_source]

distributed = <bool>
* Controls whether we will do a distributed search for show source to get
  events from all servers and indexes
* Turning this off results in better performance for show source, but events
  will only come from the initial server and index
* NOTE: event signing and verification is not supported in distributed mode
* Default: true

distributed_search_limit = <unsigned int>
* Sets a limit on the maximum events we will request when doing the search for
  distributed show source
* As this is used for a larger search than the initial non-distributed show
  source, it is larger than max_count
* Splunk will rarely return anywhere near this amount of results, as we will
  prune the excess results
* The point is to ensure the distributed search captures the target event in an
  environment with many events
* Default: 30000

max_count = <integer>
* Maximum number of events accessible by show_source.
* The show source command will fail when more than this many events are in the
  same second as the requested event.
* Default: 10000

max_timeafter = <timespan>
* Maximum time after requested event to show.
* Default: '1day' (86400 seconds)

max_timebefore = <timespan>
* Maximum time before requested event to show.
* Default: '1day' (86400 seconds)


[rex]

match_limit = <integer>
* Limits the amount of resources that are spent by PCRE
  when running patterns that will not match.
* Use this to set an upper bound on how many times PCRE calls an internal
  function, match(). If set too low, PCRE might fail to correctly match a pattern.
* Default: 100000


[slc]

maxclusters = <integer>
* Maximum number of clusters to create.
* Default: 10000.


[slow_peer_disconnect]

# This stanza contains settings for the heuristic that will detect and 
# disconnect slow peers towards the end of a search that has returned a 
# large volume of data.

batch_search_activation_fraction = <double>  
* The fraction of peers that must have completed before we start 
  disconnecting.
* This is only applicable to batch search because the slow peers will 
  not hold back the fast peers.
* Default: 0.9

bound_on_disconnect_threshold_as_fraction_of_mean = <double>
* The maximum value of the threshold data rate we will use to determine 
  if a peer is slow. The actual threshold will be computed dynamically
  at search time but will never exceed 
  (100*maximum_threshold_as_fraction_of_mean)% on either side of the mean. 
* Default: 0.2

disabled = <boolean> 
* Specifies if this feature is enabled. 
* Default: true

grace_period_before_disconnect = <double>
* If the heuristic consistently claims that the peer is slow for at least
  <grace_period_before_disconnect>*life_time_of_collector seconds then only
  will we disconnect the peer
* Default: 0.1

packets_per_data_point = <unsigned int>
* Rate statistics will be sampled once every packets_per_data_point packets.
* Default: 500

sensitivity = <double>
* Sensitivity of the heuristic to newer values. For larger values of 
  sensitivity the heuristic will give more weight to newer statistic.   
* Default: 0.3

threshold_connection_life_time = <unsigned int>
* All peers will be given an initial grace period of at least these many
  seconds before we consider them in the heuristic. 
* Default: 60

threshold_data_volume = <unsigned int>
* The volume of uncompressed data that must have accumulated, in 
  kilobytes (KB), from a peer before we consider them in the heuristic. 
* Default: 1024


[summarize]


bucket_refresh_interval = <int>
* When poll_buckets_until_maxtime is enabled in a non-clustered 
  environment, this is the minimum amount of time (in seconds) 
  between bucket refreshes.
* Default: 30

bucket_refresh_interval_cluster = <int>
* When poll_buckets_until_maxtime is enabled in a clustered 
  environment, this is the minimum amount of time (in seconds) 
  between bucket refreshes.
* Default: 120

hot_bucket_min_new_events = <integer>
* The minimum number of new events that need to be added to the hot bucket
  (since last summarization)  before a new summarization can take place. 
  To disable hot bucket summarization set this value to a * large positive 
  number.
* Default: 100000

indextime_lag = <unsigned int>
* The amount of lag time, in seconds, to give indexing to ensure that 
  it has synced any received events to disk. Effectively, the data that 
  has been received in the past “indextime_lag” will NOT be summarized.
* Do not change this value unless directed by Splunk support.
* Default: 90

max_hot_bucket_summarization_idle_time = <unsigned int>
* Maximum amount of time, in seconds, a hot bucket can be idle. When the 
  time exceeds the maximum, all of the events are summarized even if there 
  are not enough events (determined by the hot_bucket_min_new_events 
  attribute).
* Default: 900 (15 minutes)

max_replicated_hot_bucket_idle_time = <unsigned int>
* Maximum amount of time, in seconds, a replicated hot bucket can be idle 
  after which we won't apply indextime_lag. 
* This applies to only idle replicated hot buckets. As soon as new events 
  start flowing in we will revert to the default behavior of applying 
  indextime_lag
* Default: 150 

max_summary_ratio = <float>
* A number in the [0-1] range that indicates the maximum ratio of
  summary data / bucket size at which point the summarization of that 
  bucket, for the particular search, will be disabled. Use 0 to disable.
* Default: 0

max_summary_size = <int>
* Size of summary, in bytes, at which point we'll start applying the
  max_summary_ratio. Use 0 to disable.
* Default: 0

max_time = <int>
* The maximum amount of time, seconds, that a summary search process is 
  allowed to run. 
* Use 0 to disable.
* Default: 0

poll_buckets_until_maxtime = <bool>
* Only modify this setting when you are directed to do so by Support.
* Use the datamodels.conf setting acceleration.poll_buckets_until_maxtime
  for individual data models that are sensitive to summarization latency delays. 
* Default: false

sleep_seconds = <integer>
* The amount of time, in seconds, to sleep between polling of summarization 
  complete status.
* Default: 5

stale_lock_seconds = <integer>
* The amount of time, in seconds, to have elapse since the mod time of 
  a .lock file before summarization considers * that lock file stale 
  and removes it.
* Default: 600


[system_checks]

insufficient_search_capabilities = enabled | disabled
* Enables/disables automatic daily logging of scheduled searches by users
  who have insufficient capabilities to run them as configured.
* Such searches are those that:
  + Have schedule_priority set to a value other than "default" but the 
    owner does not have the edit_search_schedule_priority capability.
  + Have schedule_window set to a value other than "auto" but the owner does
    not have the edit_search_schedule_window capability.
* This check and any resulting logging occur on system startup and every 24
  hours thereafter.
* Default: enabled

installed_files_integrity = enabled | log_only | disabled
* Enables/disables automatic verification on every startup that all the 
  files that were installed with the running Splunk version are still the 
  files that should be present.
  * Effectively this finds cases where files were removed or changed that
    should not be removed or changed, whether by accident or intent.
  * The source of truth for the files that should be present is the manifest
    file in the $SPLUNK_HOME directory that comes with the release, so if 
    this file is removed or altered, the check cannot work correctly.
  * Reading of all the files provided with the install has some I/O cost,
    though it is paid out over many seconds and should not be severe.
* When "enabled", detected problems will cause a message to be posted to 
  the bulletin board (system UI status message).
* When "enabled" or "log_only", detected problems will cause details to be
  written out to splunkd.log
* When "disabled", no check will be attempted or reported.
* Default: enabled

orphan_searches = enabled|disabled
* Enables/disables automatic UI message notifications to admins for
  scheduled saved searches with invalid owners.
  * Scheduled saved searches with invalid owners are considered "orphaned".
    They cannot be run because Splunk cannot determine the roles to use for 
    the search context.
  * Typically, this situation occurs when a user creates scheduled searches
    then departs the organization or company, causing their account to be
    deactivated.
* Currently this check and any resulting notifications occur on system 
  startup and every 24 hours thereafter.
* Default: enabled


[thruput]

maxKBps = <integer>
* If specified and not zero, this limits the speed through the thruput 
  processor in the ingestion pipeline to the specified rate in kilobytes 
  per second.
* To control the CPU load while indexing, use this to throttle the number 
  of events this indexer processes to the rate (in KBps) you specify.
* Note that this limit will be applied per ingestion pipeline. For more 
  information about multiple ingestion pipelines see 
  parallelIngestionPipelines in the server.conf.spec file.
* With N parallel ingestion pipelines the thruput limit across all of the 
  ingestion pipelines will be N * maxKBps.
* Default: 0 (unlimited)


[viewstates]

enable_reaper = <boolean>
* Controls whether the viewstate reaper runs
* Default: true

reaper_freq = <integer>
* Controls how often, in seconds, the viewstate reaper runs.
* Default: 86400 (24 hours)

reaper_soft_warn_level = <integer>
* Controls what the reaper considers an acceptable number of viewstates.
* Default: 1000

ttl = <integer>
* Controls the age, in seconds, at which a viewstate is considered eligible 
  for reaping
* Default: 86400 (24 hours)


############################################################################
# OPTIMIZATION
############################################################################
# This section contains global and specific optimization settings

[search_optimization]

enabled = <bool>
* Enables search optimizations
* Default: true


[search_optimization::predicate_merge]
# NOTE: Do not edit the below configurations unless directed by support

enabled = <bool>
* Enables predicate merge optimization
* Default: true

inputlookup_merge = <bool>
* Enables predicate merge optimization to merge predicates into inputlookup
* predicate_merge must be enabled for this optimization to be performed
* Default: true


[search_optimization::predicate_push]

enabled = <bool>
* Enables predicate push optimization
* Default: true


[search_optimization::predicate_split]

enabled = <bool>
* Enables predicate split optimization
* Default: true


[search_optimization::projection_elimination]
# Configuration options for projection elimination optimization

enabled = <bool>
* Enables projection elimination optimization
* Default: true

cmds_black_list = <Commands List>
* A comma-separated list of commands that are not affected by projection 
  elimination optimization.
* Default: no default


[search_optimization::required_field_values]

enabled = <bool>
* Enables required field value optimization
* Default: true

fields = <comma-separated-string>
* Enables required field value optimizations.
* Takes a list of field names to optimize.
* When unset: required_field_values optimization is turned off.
* Default: eventtype, tag


[parallelreduce]
maxReducersPerPhase = <positive integer>
* The maximum number of indexers that can be used as reducers
  in the reducing phase.
* If a number greater than 200 or an invalid value is specified,
  the search uses the 2-phased mode.
* Default: 4

maxRunningPrdSearches = <unsigned int>
* The maximum number of parallel reduce searches that can run on
  an indexer.
* Default: 4

reducers = <string>
* Used to configure an indexer pool that is serving parallel reduce
  searches. For <string>, specify the host and port using this format
  - host:port. Separate each host:port pair with a comma to specify a
  list of reducers.
* For the reducing phase in parallel reduce search, a sub-set of
  indexers are selected from this pool and perform this phase.
* If not configured, the search head selects the indexers from the
  search head peer list.
* Default: ""

winningRate = <positive integer>
* The percentage of indexers that can be selected from the indexer
  pool for reducing phase of the parallel reduce.
* The default is 50%.
* If 100 is specified, the search head attempts to use all of the
  indexers.
* If 1 is specified, the search head attempts to use 1% of the
  indexers.
* The minimum number of indexers used in the reducing phase is 1.
  The maximum number of indexers used is the value of
  "maxReducersPerPhase.  
* Default: 50