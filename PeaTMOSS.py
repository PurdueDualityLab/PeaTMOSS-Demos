from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, relationship, Session
from sqlalchemy import inspect
from sqlalchemy.dialects.sqlite import insert

#############################################
#                                           #
#   Database Connection and Initialization  #
#                                           #
#############################################

# Shorthand for the DeclarativeBase class
# Used to create the database schema
class BASE(DeclarativeBase):
    pass

# The Model class defines the way a PTM Model is stored in the database
# It is used to create the model table
class Model(BASE):
    __tablename__ = "model"
    id = Column(Integer, primary_key=True)
    context_id = Column(Integer, unique=True)
    model_hub_id = Column(Integer, ForeignKey("model_hub.id"))
    model_hub = relationship("ModelHub", back_populates="model")
    sha = Column(String)
    repo_url = Column(String)
    downloads = Column(Integer)
    likes = Column(Integer)
    has_snapshot = Column(Integer)
    datasets = relationship("Dataset", secondary="model_to_dataset")
    architectures = relationship("Architecture", secondary="model_to_architecture")
    authors = relationship("Author", secondary="model_to_author")
    discussions = relationship("Discussion", back_populates="model")
    hf_commits = relationship("HFCommit", back_populates="model")
    hf_gitrefs = relationship("HFGitRef", back_populates="model")
    ptm_issues_id = Column(Integer, ForeignKey("ptm_issues.id"))
    ptm_issues = relationship("PTMIssues", back_populates="model")
    ptm_pull_requests_id = Column(Integer, ForeignKey("ptm_pull_requests.id"))
    ptm_pull_requests = relationship("PTMPullRequests", back_populates="model")
    frameworks = relationship("Framework", secondary="model_to_framework")
    languages = relationship("Language", secondary="model_to_language")
    libraries = relationship("Library", secondary="model_to_library")
    licenses = relationship("License", secondary="model_to_license")
    papers = relationship("Paper", secondary="model_to_paper")
    reuse_repositories = relationship("ReuseRepository", secondary="model_to_reuse_repository")
    tags = relationship("Tag", secondary="model_to_tag")

# The PTMIssues class as an aggregator for the issues associated with the PTMs
class PTMIssues(BASE):
    __tablename__ = "ptm_issues"
    id = Column(Integer, primary_key=True)
    repo_url = Column(String, unique=True)
    issues = relationship("GitHubIssue", secondary="ptm_issue_to_issue")
    model = relationship("Model", back_populates="ptm_issues")

# ptm_issue_to_issue is used to create the one-to-many relationship between the ptm_issues table and the github_issue table
ptm_issue_to_issue = Table(
    "ptm_issue_to_issue",
    BASE.metadata,
    Column("ptm_issue_id", Integer, ForeignKey("ptm_issues.id"), primary_key=True),
    Column("github_issue_id", Integer, ForeignKey("github_issue.id"), primary_key=True),
)

# The PTMPullRequests class as an aggregator for the pull requests associated with the PTMs
class PTMPullRequests(BASE):
    __tablename__ = "ptm_pull_requests"
    id = Column(Integer, primary_key=True)
    repo_url = Column(String, unique=True)
    pull_requests = relationship("GitHubPullRequest", secondary="ptm_pull_request_to_pull_request")
    model = relationship("Model", back_populates="ptm_pull_requests")

# ptm_pull_request_to_pull_request is used to create the one-to-many relationship between the ptm_pull_requests table and the github_pull_request table
ptm_pull_request_to_pull_request = Table(
    "ptm_pull_request_to_pull_request",
    BASE.metadata,
    Column("ptm_pull_request_id", Integer, ForeignKey("ptm_pull_requests.id"), primary_key=True),
    Column("github_pull_request_id", Integer, ForeignKey("github_pull_request.id"), primary_key=True),
)

# The HFCommit class stores commit info about a model stored on HuggingFace
class HFCommit(BASE):
    __tablename__ = "hf_commit"
    id = Column(Integer, primary_key=True)
    commit_id = Column(String)
    authors = relationship("Author", secondary="hf_commit_to_author")
    created_at = Column(String)
    title = Column(String)
    message = Column(String)
    model_id = Column(Integer, ForeignKey("model.id"))
    model = relationship("Model", back_populates="hf_commits")

# hf_commit_to_author is used to create the many-to-many relationship between the hf_commit table and the author table
hf_commit_to_author = Table(
    "hf_commit_to_author",
    BASE.metadata,
    Column("hf_commit_id", Integer, ForeignKey("hf_commit.id"), primary_key=True),
    Column("author_id", Integer, ForeignKey("author.id"), primary_key=True),
)

# The HFGitRef class stores git ref info about a model stored on HuggingFace
class HFGitRef(BASE):
    __tablename__ = "hf_git_ref"
    id = Column(Integer, primary_key=True)
    branches = relationship("HFGitRefInfo", secondary="hf_git_ref_to_branch")
    tags = relationship("HFGitRefInfo", secondary="hf_git_ref_to_tag")
    model_id = Column(Integer, ForeignKey("model.id"))
    model = relationship("Model", back_populates="hf_gitrefs")

# hf_git_ref_to_branch is used to create the one-to-many relationship between the hf_git_ref table and the hf_git_ref_info table, specifically to describe the branches
hf_git_ref_to_branch = Table(
    "hf_git_ref_to_branch",
    BASE.metadata,
    Column("hf_git_ref_id", Integer, ForeignKey("hf_git_ref.id"), primary_key=True),
    Column("hf_git_ref_info_id", Integer, ForeignKey("hf_git_ref_info.id"), primary_key=True),
)

# hf_git_ref_to_tag is used to create the one-to-many relationship between the hf_git_ref table and the hf_git_ref_info table, specifically to describe the tags
hf_git_ref_to_tag = Table(
    "hf_git_ref_to_tag",
    BASE.metadata,
    Column("hf_git_ref_id", Integer, ForeignKey("hf_git_ref.id"), primary_key=True),
    Column("hf_git_ref_info_id", Integer, ForeignKey("hf_git_ref_info.id"), primary_key=True),
)

# The HFGitRefInfo class stores info about a branch or tag associated with a model stored on HuggingFace
class HFGitRefInfo(BASE):
    __tablename__ = "hf_git_ref_info"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    ref = Column(String)
    target_commit = Column(String)

# The ModelHub class stores info about the model hub where a model is stored
class ModelHub(BASE):
    __tablename__ = "model_hub"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    url = Column(String, unique=True)
    model = relationship("Model", back_populates="model_hub")

#############################################
#                                           #
#   The following tables are used to        #
#   create the many-to-many relationships   #
#   between the model table and the         #
#   tables:                                 #
#   architecture, author, framework,        #
#   language, library, license, paper,      #
#   tag                                     #
#                                           #
#############################################

# model_to_architecture is used to create the many-to-many relationship between the model table and the architecture table
model_to_architecture = Table(
    "model_to_architecture",
    BASE.metadata,
    Column("model_id", Integer, ForeignKey("model.id"), primary_key=True),
    Column("architecture_id", Integer, ForeignKey("architecture.id"), primary_key=True),
)

# model_to_author is used to create the many-to-many relationship between the model table and the author table
model_to_author = Table(
    "model_to_author",
    BASE.metadata,
    Column("model_id", Integer, ForeignKey("model.id"), primary_key=True),
    Column("author_id", Integer, ForeignKey("author.id"), primary_key=True),
)

# model_to_dataset is used to create the many-to-many relationship between the model table and the dataset table
model_to_dataset = Table(
    "model_to_dataset",
    BASE.metadata,
    Column("model_id", Integer, ForeignKey("model.id"), primary_key=True),
    Column("dataset_id", Integer, ForeignKey("dataset.id"), primary_key=True),
)

# model_to_framework is used to create the many-to-many relationship between the model table and the framework table
model_to_framework = Table(
    "model_to_framework",
    BASE.metadata,
    Column("model_id", Integer, ForeignKey("model.id"), primary_key=True),
    Column("framework_id", Integer, ForeignKey("framework.id"), primary_key=True),
)

# model_to_language is used to create the many-to-many relationship between the model table and the language table
model_to_language = Table(
    "model_to_language",
    BASE.metadata,
    Column("model_id", Integer, ForeignKey("model.id"), primary_key=True),
    Column("language_id", Integer, ForeignKey("language.id"), primary_key=True),
)

# model_to_library is used to create the many-to-many relationship between the model table and the library table
model_to_library = Table(
    "model_to_library",
    BASE.metadata,
    Column("model_id", Integer, ForeignKey("model.id"), primary_key=True),
    Column("library_id", Integer, ForeignKey("library.id"), primary_key=True),
)

# model_to_license is used to create the many-to-many relationship between the model table and the license table
model_to_license = Table(
    "model_to_license",
    BASE.metadata,
    Column("model_id", Integer, ForeignKey("model.id"), primary_key=True),
    Column("license_id", Integer, ForeignKey("license.id"), primary_key=True),
)

# model_to_paper is used to create the many-to-many relationship between the model table and the paper table
model_to_paper = Table(
    "model_to_paper",
    BASE.metadata,
    Column("model_id", Integer, ForeignKey("model.id"), primary_key=True),
    Column("paper_id", Integer, ForeignKey("paper.id"), primary_key=True),
)

# model_to_tag is used to create the many-to-many relationship between the model table and the tag table
model_to_tag = Table(
    "model_to_tag",
    BASE.metadata,
    Column("model_id", Integer, ForeignKey("model.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tag.id"), primary_key=True),
)

#############################################
#                                           #
#   The following tables contain more       #
#   metadata about the model                #
#                                           #
#############################################

# The architecture table contains the architectures used by the model
class Architecture(BASE):
    __tablename__ = "architecture"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

# The author table contains the authors of the model
class Author(BASE):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

# The Dataset table contains the datasets used by the model
class Dataset(BASE):
    __tablename__ = "dataset"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

# The framework table contains the frameworks used by the model
class Framework(BASE):
    __tablename__ = "framework"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

# The language table contains the languages used by the model
class Language(BASE):
    __tablename__ = "language"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    abbreviation = Column(String, unique=True)

# The library table contains the libraries used by the model
class Library(BASE):
    __tablename__ = "library"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

# The license table contains the licenses used by the model
class License(BASE):
    __tablename__ = "license"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

# The paper table contains the papers used by the model
class Paper(BASE):
    __tablename__ = "paper"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

# The tag table contains the tags used by the model
class Tag(BASE):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

#############################################
#                                           #
#   The following tables contain            #
#   HuggingFace Discussions and their       #
#   associated metadata                     #
#                                           #
#############################################

# The discussion table contains the discussions stored on HuggingFace for each model
class Discussion(BASE):
    __tablename__ = "discussion"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    status = Column(String)
    num = Column(Integer)
    repo_id = Column(String)
    repo_type = Column(String)
    author = relationship("Author", secondary="discussion_to_author")
    is_pull_request = Column(Integer)
    created_at = Column(String)
    endpoint = Column(String)
    conflicting_files = relationship("FilePath", back_populates="discussion")
    target_branch = Column(String)
    merge_commit_oid = Column(String)
    diff = Column(String)
    model_id = Column(Integer, ForeignKey("model.id"))
    model = relationship("Model", back_populates="discussions")
    events = relationship("DiscussionEvent", back_populates="discussion")

# discussion_to_author is used to create the many-to-many relationship between the discussion table and the author table
discussion_to_author = Table(
    "discussion_to_author",
    BASE.metadata,
    Column("discussion_id", Integer, ForeignKey("discussion.id"), primary_key=True),
    Column("author_id", Integer, ForeignKey("author.id"), primary_key=True)
)

# This table contains the filepaths for any files references by a pull request
class FilePath(BASE):
    __tablename__ = "file_path"
    id = Column(Integer, primary_key=True)
    path = Column(String)
    discussion_id = Column(Integer, ForeignKey("discussion.id"))
    discussion = relationship("Discussion", back_populates="conflicting_files")

# This table contains the events associated with a discussion
# There are 4 different types of events:
#   - Discussion Created
#   - Discussion Edited
#   - Discussion Comment
#   - Discussion Status Changed
# Each only uses a subset of the columns in this table
class DiscussionEvent(BASE):
    __tablename__ = "discussion_event"
    id = Column(Integer, primary_key=True)
    event_id = Column(String)
    type = Column(String)
    created_at = Column(String)
    author = Column(String)
    content = Column(String)
    edited = Column(Integer)
    hidden = Column(Integer)
    new_status = Column(String)
    summary = Column(String)
    oid = Column(String)
    old_title = Column(String)
    new_title = Column(String)
    discussion_id = Column(Integer, ForeignKey("discussion.id"))
    discussion = relationship("Discussion", back_populates="events")

#############################################
#                                           #
#   The following tables contain            #
#   metadata about Open Source GitHub       #
#   repositories that use the PTMs          #
#   whose metadata is stored in the         #
#   model table                             #
#                                           #
#############################################

# The reuse_repository table contains the repositories that use the PTMs
class ReuseRepository(BASE):
    __tablename__ = "reuse_repository"
    id = Column(Integer, primary_key=True)
    owner = Column(String)
    name = Column(String)
    url = Column(String)
    issues = relationship("GitHubIssue", secondary="reuse_repo_to_issue", back_populates="reuse_repository")
    pull_requests = relationship("GitHubPullRequest", secondary="reuse_repo_to_pull_request", back_populates="reuse_repository")
    files = relationship("ReuseFile", back_populates="reuse_repository")

    __table_args__ = (
        UniqueConstraint("owner", "name", name="unique_owner_name"),
    )

# reuse_repo_to_issue is used to create the many-to-many relationship between the reuse_repository table and the github_issue table
reuse_repo_to_issue = Table(
    "reuse_repo_to_issue",
    BASE.metadata,
    Column("reuse_repository_id", Integer, ForeignKey("reuse_repository.id"), primary_key=True),
    Column("github_issue_id", Integer, ForeignKey("github_issue.id"), primary_key=True),
)

# reuse_repo_to_pull_request is used to create the many-to-many relationship between the reuse_repository table and the github_pull_request table
reuse_repo_to_pull_request = Table(
    "reuse_repo_to_pull_request",
    BASE.metadata,
    Column("reuse_repository_id", Integer, ForeignKey("reuse_repository.id"), primary_key=True),
    Column("github_pull_request_id", Integer, ForeignKey("github_pull_request.id"), primary_key=True),
)

# The reuse_file table contains the specific files in the reuse repositories that use the PTMs
class ReuseFile(BASE):
    __tablename__ = "reuse_file"
    id = Column(Integer, primary_key=True)
    path = Column(String)
    model_id = Column(Integer, ForeignKey("model.id"))
    model = relationship("Model")
    reuse_repository_id = Column(Integer, ForeignKey("reuse_repository.id"))
    reuse_repository = relationship("ReuseRepository", back_populates="files")

    __table_args__ = (
        UniqueConstraint("path", "model_id", name="unique_path_model_id"),
    )

# model_to_reuse_repository is used to create the many-to-many relationship between the model table and the reuse_repository table
model_to_reuse_repository = Table(
    "model_to_reuse_repository",
    BASE.metadata,
    Column("model_id", Integer, ForeignKey("model.id"), primary_key=True),
    Column("reuse_repository_id", Integer, ForeignKey("reuse_repository.id"), primary_key=True),
)

#############################################
#                                           #
#   The following tables contain            #
#   metadata about the issues and           #
#   pull requests associated with           #
#   GitHub repositories                     #
#                                           #
############################################

# The github_issue table contains the issues associated with the reuse repositories
class GitHubIssue(BASE):
    __tablename__ = "github_issue"
    id = Column(Integer, primary_key=True)
    assignee = relationship("GitHubUser", secondary="issue_to_assignee")
    author_id = Column(Integer, ForeignKey("github_user.id"))
    author = relationship("GitHubUser", foreign_keys=[author_id])
    body = Column(String)
    closed = Column(Integer)
    closed_at = Column(String)
    comments = relationship("GitHubComment", back_populates="issue")
    created_at = Column(String)
    comment_id = Column(String)
    labels = relationship("GitHubLabel", back_populates="issue")
    milestone_id = Column(Integer, ForeignKey("github_milestone.id"))
    milestone = relationship("GitHubMilestone", foreign_keys=[milestone_id])
    number = Column(Integer)
    project_cards = Column(String)
    reaction_groups = relationship("GitHubReactionGroup", back_populates="issue")
    state = Column(String)
    title = Column(String)
    updated_at = Column(String)
    url = Column(String, unique=True)
    reuse_repository = relationship("ReuseRepository", secondary="reuse_repo_to_issue", back_populates="issues")

# issue_to_assignee is used to create the many-to-many relationship between the github_issue table and the github_user table
issue_to_assignee = Table(
    "issue_to_assignee",
    BASE.metadata,
    Column("issue_id", Integer, ForeignKey("github_issue.id"), primary_key=True),
    Column("assignee_id", Integer, ForeignKey("github_user.id"), primary_key=True),
)

# The github_pull_request table contains the pull requests associated with the reuse repositories
class GitHubPullRequest(BASE):
    __tablename__ = "github_pull_request"
    id = Column(Integer, primary_key=True)
    additions = Column(Integer)
    assignees = relationship("GitHubUser", secondary="pull_request_to_assignee")
    author_id = Column(Integer, ForeignKey("github_user.id"))
    author = relationship("GitHubUser", foreign_keys=[author_id])
    base_ref_name = Column(String)
    body = Column(String)
    changed_files = Column(Integer)
    closed = Column(Integer)
    closed_at = Column(String)
    comments = relationship("GitHubComment", back_populates="pull_request")
    commits = relationship("GitHubCommit", back_populates="pull_request")
    created_at = Column(String)
    deletions = Column(Integer)
    files = relationship("GitHubPullRequestFile", back_populates="pull_request")
    head_ref_name = Column(String)
    head_repository_id = Column(Integer, ForeignKey("github_repository.id"))
    head_repository = relationship("GitHubRepository", foreign_keys=[head_repository_id])
    head_repository_owner_id = Column(Integer, ForeignKey("github_user.id"))
    head_repository_owner = relationship("GitHubUser", foreign_keys=[head_repository_owner_id])
    is_cross_repository = Column(Integer)
    is_draft = Column(Integer)
    labels = relationship("GitHubLabel", back_populates="pull_request")
    maintainer_can_modify = Column(Integer)
    merge_commit_id = Column(Integer, ForeignKey("github_merge_commit.id"))
    merge_commit = relationship("GitHubMergeCommit", foreign_keys=[merge_commit_id])
    merge_state_status = Column(String)
    mergeable = Column(String)
    merged_at = Column(String)
    merged_by_id = Column(Integer, ForeignKey("github_user.id"))
    merged_by = relationship("GitHubUser", foreign_keys=[merged_by_id])
    milestone_id = Column(Integer, ForeignKey("github_milestone.id"))
    milestone = relationship("GitHubMilestone", foreign_keys=[milestone_id])
    number = Column(Integer)
    potential_merge_commit_id = Column(Integer, ForeignKey("github_merge_commit.id"))
    potential_merge_commit = relationship("GitHubMergeCommit", foreign_keys=[potential_merge_commit_id])
    project_cards = Column(String)
    reaction_groups = relationship("GitHubReactionGroup", back_populates="pull_request")
    review_decision = Column(String)
    review_requests = relationship("GitHubUser", secondary="pull_request_to_review_requests")
    reviews = relationship("GitHubReview", back_populates="pull_request")
    state = Column(String)
    status_check_rollup = relationship("GitHubStatusCheckRollup", back_populates="pull_request")
    title = Column(String)
    updated_at = Column(String)
    url = Column(String, unique=True)
    reuse_repository = relationship("ReuseRepository", secondary="reuse_repo_to_pull_request", back_populates="pull_requests")

# github_pull_request_file contains the files that were changed in a pull request
class GitHubPullRequestFile(BASE):
    __tablename__ = "github_pull_request_file"
    id = Column(Integer, primary_key=True)
    path = Column(String)
    additions = Column(Integer)
    deletions = Column(Integer)
    pull_request_id = Column(Integer, ForeignKey("github_pull_request.id"))
    pull_request = relationship("GitHubPullRequest", back_populates="files")

# pull_request_to_assignee is used to create the many-to-many relationship between the github_pull_request table and the github_user table
pull_request_to_assignee = Table(
    "pull_request_to_assignee",
    BASE.metadata,
    Column("pull_request_id", Integer, ForeignKey("github_pull_request.id"), primary_key=True),
    Column("assignee_id", Integer, ForeignKey("github_user.id"), primary_key=True)
)

# pull_request_to_review_requests is used to create the many-to-many relationship between the github_pull_request table and the github_user table
pull_request_to_review_requests = Table(
    "pull_request_to_review_requests",
    BASE.metadata,
    Column("pull_request_id", Integer, ForeignKey("github_pull_request.id"), primary_key=True),
    Column("review_request_id", Integer, ForeignKey("github_user.id"), primary_key=True)
)

# The github_comment table contains the comments associated with the issues and pull requests
class GitHubComment(BASE):
    __tablename__ = "github_comment"
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("github_user.id"))
    author = relationship("GitHubUser", foreign_keys=[author_id])
    author_association = Column(String)
    body = Column(String)
    created_at = Column(String)
    includes_created_edit = Column(Integer)
    is_minimized = Column(Integer)
    minimized_reason = Column(String)
    reaction_groups = relationship("GitHubReactionGroup", back_populates="github_comment")
    issue_id = Column(Integer, ForeignKey("github_issue.id"))
    issue = relationship("GitHubIssue", back_populates="comments")
    pull_request_id = Column(Integer, ForeignKey("github_pull_request.id"))
    pull_request = relationship("GitHubPullRequest", back_populates="comments")

# The github_commit table contains the commits associated with the pull requests
class GitHubCommit(BASE):
    __tablename__ = "github_commit"
    id = Column(Integer, primary_key=True)
    authored_date = Column(String)
    authors = relationship("GitHubUser", secondary="commit_to_author")
    committed_date = Column(String)
    message_body = Column(String)
    message_headline = Column(String)
    oid = Column(String)
    pull_request_id = Column(Integer, ForeignKey("github_pull_request.id"))
    pull_request = relationship("GitHubPullRequest", back_populates="commits")

# commit_to_author is used to create the many-to-many relationship between the github_commit table and the github_user table
commit_to_author = Table(
    "commit_to_author",
    BASE.metadata,
    Column("commit_id", Integer, ForeignKey("github_commit.id"), primary_key=True),
    Column("author_id", Integer, ForeignKey("github_user.id"), primary_key=True)
)

# The github_label table contains the labels associated with the issues and pull requests
class GitHubLabel(BASE):
    __tablename__ = "github_label"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    color = Column(String)
    issue_id = Column(Integer, ForeignKey("github_issue.id"))
    issue = relationship("GitHubIssue", back_populates="labels")
    pull_request_id = Column(Integer, ForeignKey("github_pull_request.id"))
    pull_request = relationship("GitHubPullRequest", back_populates="labels")

# The github_merge_commit table contains the merge commits associated with the pull requests
# It prevents there being a foreign key constraint on the github_commit table since there are many commits that are not merge commits
class GitHubMergeCommit(BASE):
    __tablename__ = "github_merge_commit"
    id = Column(Integer, primary_key=True)
    commit_id = Column(Integer, ForeignKey("github_commit.id"))
    commit = relationship("GitHubCommit", foreign_keys=[commit_id])

# The github_milestone table contains the milestones associated with the issues and pull requests
class GitHubMilestone(BASE):
    __tablename__ = "github_milestone"
    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    title = Column(String)
    description = Column(String)
    due_on = Column(String)

# The github_reaction_group table contains the reaction groups associated with issues, pull requests, comments, and reviews
class GitHubReactionGroup(BASE):
    __tablename__ = "github_reaction_group"
    id = Column(Integer, primary_key=True)
    content = Column(String)
    total_count = Column(Integer)
    issue_id = Column(Integer, ForeignKey("github_issue.id"))
    issue = relationship("GitHubIssue", back_populates="reaction_groups")
    pull_request_id = Column(Integer, ForeignKey("github_pull_request.id"))
    pull_request = relationship("GitHubPullRequest", back_populates="reaction_groups")
    github_comment_id = Column(Integer, ForeignKey("github_comment.id"))
    github_comment = relationship("GitHubComment", back_populates="reaction_groups")
    review_id = Column(Integer, ForeignKey("github_review.id"))
    review = relationship("GitHubReview", back_populates="reaction_groups")

# The github_repository table contains the repositories associated with the pull requests
class GitHubRepository(BASE):
    __tablename__ = "github_repository"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)

# The github_review table contains the reviews associated with the pull requests
class GitHubReview(BASE):
    __tablename__ = "github_review"
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("github_user.id"))
    author = relationship("GitHubUser", foreign_keys=[author_id])
    author_association = Column(String)
    body = Column(String)
    submitted_at = Column(String)
    includes_created_edit = Column(Integer)
    reaction_groups = relationship("GitHubReactionGroup", back_populates="review")
    state = Column(String)
    pull_request_id = Column(Integer, ForeignKey("github_pull_request.id"))
    pull_request = relationship("GitHubPullRequest", back_populates="reviews")

# The github_status_check_rollup table contains the status check rollups associated with the pull requests
class GitHubStatusCheckRollup(BASE):
    __tablename__ = "github_status_check_rollup"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    status = Column(String)
    conclusion = Column(String)
    started_at = Column(String)
    completed_at = Column(String)
    details_url = Column(String)
    pull_request_id = Column(Integer, ForeignKey("github_pull_request.id"))
    pull_request = relationship("GitHubPullRequest", back_populates="status_check_rollup")

# The github_user table contains the users associated with the issues, pull requests, comments, and reviews
class GitHubUser(BASE):
    __tablename__ = "github_user"
    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True)
    email = Column(String)
    name = Column(String)