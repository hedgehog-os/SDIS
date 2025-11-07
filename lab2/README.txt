Attachment 6 10 -> Document
CheckList 5 9 -> Form
Document 15 22 -> Attachment, Revision, Comment, Template, Keyword, Form, Protocol, Report, Metadata
Draft 5 6 -> Reviewer
ExperimentLog 6 7 -> ExternalExpert
Form 6 6 -> CheckList
Protocol 6 7 -> Supervisor
Report 8 12 -> Chart, Summary, CommitteeMember, Comment
Revision 9 8 -> Editor
Template 8 8 -> Document, Attachment, Revision, Comment, Keyword
Calibration 4 10 -> Documet, Revision,  Report Comment
CaseTest 6 7 -> Procedure, Measurements
Chemical 5 12 -> Reaction
Device 2 7 -> Calibration
Experiment 5 9 -> CaseTest, Procedure
LabRoom 2 8 -> Device
Measurement 4 4 -> Sensor
Procedure 5 7 -> CaseTest, Measurement
Reaction 6 9 -> Chemical
Sample 3 5 -> Chemical
Sensor 3 5 -> Device
StorageDevice 6 9 -> Backup
Annotation 5 5 -> 
Chart 4 12 -> Report
Comment 6 5 -> 
Dataset 4 12 -> Report
Insight 3 10 -> Report
Keyword 2 10 -> Insight, Document
Metadata 8 14 -> Document
Statistics 4 13 -> Metadata, Revision, Report, Document
Summary 4 11 -> Report, Insight, Chart, Document, Keyword
Tag 4 13 -> Document, Metadata, Insight, Report
Author 5 10 -> Document, Revision, Report, Comment
CommitteeMember 6 7 -> Report
Editor 6 8 -> 
ExternalExpert 9 12 -> 
LabAssistant 6 11 -> LabRoom, Experiment, Device
Observer 5 8 -> 
Reviewer 6 7 -> Draft
Student 7 10 -> UserProfile
Supervisor 4 8 -> Document
UserProfile 11 12 -> 
AccessLog 5 11 -> UserProfile, Document
Archive 4 16 -> Document, Backup, StorageDevice, Report, Form
Backup 6 9 -> Encryption, StorageDevice
CloudStorage 3 12 -> Backup
Encryption 5 6 -> Backup
Folder 4 15 -> Document, Report, Archive
LocalStorage 2 11 -> Backup, Folder, Document
Permission 5 15 -> UserProfile, Document, AccessLog
SecurityPolicy 4 12 -> Document, Permission
VersionControl 3 8 ->

Exceptions(14):
DocumentNotReadyError 0 0 -> 
DocumentAlreadyArchivedError 0 0 ->
DocumentRestoreError 0 0 ->
ReportReviewerNotAssignedError 0 0 ->
ReportChartNotFoundError 0 0 ->
EmailFormatError 0 0 ->
PhoneNumberFormatError 0 0 ->
SecurityQuestionEmptyError 0 0 ->
MetadataTagConflictError 0 0 ->
MetadataEncryptionError 0 0 ->
MetadataDecryptionError 0 0 ->
MetadataKeywordNotFoundError 0 0 ->
ArchiveDocumentNotFoundError 0 0 ->
ArchiveAlreadyContainsDocumentError 0 0 ->

Поля: 269
Поведения: 500
Исключения: 14
