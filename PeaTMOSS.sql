CREATE TABLE ptm_issues (
        id INTEGER NOT NULL, 
        repo_url VARCHAR, 
        PRIMARY KEY (id), 
        UNIQUE (repo_url)
);
CREATE TABLE ptm_pull_requests (
        id INTEGER NOT NULL, 
        repo_url VARCHAR, 
        PRIMARY KEY (id), 
        UNIQUE (repo_url)
);
CREATE TABLE hf_git_ref_info (
        id INTEGER NOT NULL, 
        name VARCHAR, 
        ref VARCHAR, 
        target_commit VARCHAR, 
        PRIMARY KEY (id)
);
CREATE TABLE model_hub (
        id INTEGER NOT NULL, 
        name VARCHAR, 
        url VARCHAR, 
        PRIMARY KEY (id), 
        UNIQUE (name), 
        UNIQUE (url)
);
CREATE TABLE architecture (
        id INTEGER NOT NULL, 
        name VARCHAR, 
        PRIMARY KEY (id), 
        UNIQUE (name)
);
CREATE TABLE author (
        id INTEGER NOT NULL, 
        name VARCHAR, 
        PRIMARY KEY (id), 
        UNIQUE (name)
);
CREATE TABLE dataset (
        id INTEGER NOT NULL, 
        name VARCHAR, 
        PRIMARY KEY (id), 
        UNIQUE (name)
);
CREATE TABLE framework (
        id INTEGER NOT NULL, 
        name VARCHAR, 
        PRIMARY KEY (id), 
        UNIQUE (name)
);
CREATE TABLE language (
        id INTEGER NOT NULL, 
        name VARCHAR, 
        abbreviation VARCHAR, 
        PRIMARY KEY (id), 
        UNIQUE (name), 
        UNIQUE (abbreviation)
);
CREATE TABLE library (
        id INTEGER NOT NULL, 
        name VARCHAR, 
        PRIMARY KEY (id), 
        UNIQUE (name)
);
CREATE TABLE license (
        id INTEGER NOT NULL, 
        name VARCHAR, 
        PRIMARY KEY (id), 
        UNIQUE (name)
);
CREATE TABLE paper (
        id INTEGER NOT NULL, 
        name VARCHAR, 
        PRIMARY KEY (id), 
        UNIQUE (name)
);
CREATE TABLE tag (
        id INTEGER NOT NULL, 
        name VARCHAR, 
        PRIMARY KEY (id), 
        UNIQUE (name)
);
CREATE TABLE reuse_repository (
        id INTEGER NOT NULL, 
        owner VARCHAR, 
        name VARCHAR, 
        url VARCHAR, 
        PRIMARY KEY (id), 
        CONSTRAINT unique_owner_name UNIQUE (owner, name)
);
CREATE TABLE github_pull_request (
        id INTEGER NOT NULL, 
        additions INTEGER, 
        author_id INTEGER, 
        base_ref_name VARCHAR, 
        body VARCHAR, 
        changed_files INTEGER, 
        closed INTEGER, 
        closed_at VARCHAR, 
        created_at VARCHAR, 
        deletions INTEGER, 
        head_ref_name VARCHAR, 
        head_repository_id INTEGER, 
        head_repository_owner_id INTEGER, 
        is_cross_repository INTEGER, 
        is_draft INTEGER, 
        maintainer_can_modify INTEGER, 
        merge_commit_id INTEGER, 
        merge_state_status VARCHAR, 
        mergeable VARCHAR, 
        merged_at VARCHAR, 
        merged_by_id INTEGER, 
        milestone_id INTEGER, 
        number INTEGER, 
        potential_merge_commit_id INTEGER, 
        project_cards VARCHAR, 
        review_decision VARCHAR, 
        state VARCHAR, 
        title VARCHAR, 
        updated_at VARCHAR, 
        url VARCHAR, 
        PRIMARY KEY (id), 
        FOREIGN KEY(author_id) REFERENCES github_user (id), 
        FOREIGN KEY(head_repository_id) REFERENCES github_repository (id), 
        FOREIGN KEY(head_repository_owner_id) REFERENCES github_user (id), 
        FOREIGN KEY(merge_commit_id) REFERENCES github_merge_commit (id), 
        FOREIGN KEY(merged_by_id) REFERENCES github_user (id), 
        FOREIGN KEY(milestone_id) REFERENCES github_milestone (id), 
        FOREIGN KEY(potential_merge_commit_id) REFERENCES github_merge_commit (id), 
        UNIQUE (url)
);
CREATE TABLE github_commit (
        id INTEGER NOT NULL, 
        authored_date VARCHAR, 
        committed_date VARCHAR, 
        message_body VARCHAR, 
        message_headline VARCHAR, 
        oid VARCHAR, 
        pull_request_id INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(pull_request_id) REFERENCES github_pull_request (id)
);
CREATE TABLE github_merge_commit (
        id INTEGER NOT NULL, 
        commit_id INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(commit_id) REFERENCES github_commit (id)
);
CREATE TABLE github_milestone (
        id INTEGER NOT NULL, 
        number INTEGER, 
        title VARCHAR, 
        description VARCHAR, 
        due_on VARCHAR, 
        PRIMARY KEY (id)
);
CREATE TABLE github_repository (
        id INTEGER NOT NULL, 
        name VARCHAR, 
        url VARCHAR, 
        PRIMARY KEY (id)
);
CREATE TABLE github_user (
        id INTEGER NOT NULL, 
        login VARCHAR, 
        email VARCHAR, 
        name VARCHAR, 
        PRIMARY KEY (id), 
        UNIQUE (login)
);
CREATE TABLE model (
        id INTEGER NOT NULL, 
        context_id INTEGER, 
        model_hub_id INTEGER, 
        sha VARCHAR, 
        repo_url VARCHAR, 
        downloads INTEGER, 
        likes INTEGER, 
        has_snapshot INTEGER, 
        ptm_issues_id INTEGER, 
        ptm_pull_requests_id INTEGER, 
        PRIMARY KEY (id), 
        UNIQUE (context_id), 
        FOREIGN KEY(model_hub_id) REFERENCES model_hub (id), 
        FOREIGN KEY(ptm_issues_id) REFERENCES ptm_issues (id), 
        FOREIGN KEY(ptm_pull_requests_id) REFERENCES ptm_pull_requests (id)
);
CREATE TABLE ptm_pull_request_to_pull_request (
        ptm_pull_request_id INTEGER NOT NULL, 
        github_pull_request_id INTEGER NOT NULL, 
        PRIMARY KEY (ptm_pull_request_id, github_pull_request_id), 
        FOREIGN KEY(ptm_pull_request_id) REFERENCES ptm_pull_requests (id), 
        FOREIGN KEY(github_pull_request_id) REFERENCES github_pull_request (id)
);
CREATE TABLE reuse_repo_to_pull_request (
        reuse_repository_id INTEGER NOT NULL, 
        github_pull_request_id INTEGER NOT NULL, 
        PRIMARY KEY (reuse_repository_id, github_pull_request_id), 
        FOREIGN KEY(reuse_repository_id) REFERENCES reuse_repository (id), 
        FOREIGN KEY(github_pull_request_id) REFERENCES github_pull_request (id)
);
CREATE TABLE github_issue (
        id INTEGER NOT NULL, 
        author_id INTEGER, 
        body VARCHAR, 
        closed INTEGER, 
        closed_at VARCHAR, 
        created_at VARCHAR, 
        comment_id VARCHAR, 
        milestone_id INTEGER, 
        number INTEGER, 
        project_cards VARCHAR, 
        state VARCHAR, 
        title VARCHAR, 
        updated_at VARCHAR, 
        url VARCHAR, 
        PRIMARY KEY (id), 
        FOREIGN KEY(author_id) REFERENCES github_user (id), 
        FOREIGN KEY(milestone_id) REFERENCES github_milestone (id), 
        UNIQUE (url)
);
CREATE TABLE github_pull_request_file (
        id INTEGER NOT NULL, 
        path VARCHAR, 
        additions INTEGER, 
        deletions INTEGER, 
        pull_request_id INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(pull_request_id) REFERENCES github_pull_request (id)
);
CREATE TABLE pull_request_to_assignee (
        pull_request_id INTEGER NOT NULL, 
        assignee_id INTEGER NOT NULL, 
        PRIMARY KEY (pull_request_id, assignee_id), 
        FOREIGN KEY(pull_request_id) REFERENCES github_pull_request (id), 
        FOREIGN KEY(assignee_id) REFERENCES github_user (id)
);
CREATE TABLE pull_request_to_review_requests (
        pull_request_id INTEGER NOT NULL, 
        review_request_id INTEGER NOT NULL, 
        PRIMARY KEY (pull_request_id, review_request_id), 
        FOREIGN KEY(pull_request_id) REFERENCES github_pull_request (id), 
        FOREIGN KEY(review_request_id) REFERENCES github_user (id)
);
CREATE TABLE commit_to_author (
        commit_id INTEGER NOT NULL, 
        author_id INTEGER NOT NULL, 
        PRIMARY KEY (commit_id, author_id), 
        FOREIGN KEY(commit_id) REFERENCES github_commit (id), 
        FOREIGN KEY(author_id) REFERENCES github_user (id)
);
CREATE TABLE github_review (
        id INTEGER NOT NULL, 
        author_id INTEGER, 
        author_association VARCHAR, 
        body VARCHAR, 
        submitted_at VARCHAR, 
        includes_created_edit INTEGER, 
        state VARCHAR, 
        pull_request_id INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(author_id) REFERENCES github_user (id), 
        FOREIGN KEY(pull_request_id) REFERENCES github_pull_request (id)
);
CREATE TABLE github_status_check_rollup (
        id INTEGER NOT NULL, 
        name VARCHAR, 
        status VARCHAR, 
        conclusion VARCHAR, 
        started_at VARCHAR, 
        completed_at VARCHAR, 
        details_url VARCHAR, 
        pull_request_id INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(pull_request_id) REFERENCES github_pull_request (id)
);
CREATE TABLE ptm_issue_to_issue (
        ptm_issue_id INTEGER NOT NULL, 
        github_issue_id INTEGER NOT NULL, 
        PRIMARY KEY (ptm_issue_id, github_issue_id), 
        FOREIGN KEY(ptm_issue_id) REFERENCES ptm_issues (id), 
        FOREIGN KEY(github_issue_id) REFERENCES github_issue (id)
);
CREATE TABLE hf_commit (
        id INTEGER NOT NULL, 
        commit_id VARCHAR, 
        created_at VARCHAR, 
        title VARCHAR, 
        message VARCHAR, 
        model_id INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(model_id) REFERENCES model (id)
);
CREATE TABLE hf_git_ref (
        id INTEGER NOT NULL, 
        model_id INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(model_id) REFERENCES model (id)
);
CREATE TABLE model_to_architecture (
        model_id INTEGER NOT NULL, 
        architecture_id INTEGER NOT NULL, 
        PRIMARY KEY (model_id, architecture_id), 
        FOREIGN KEY(model_id) REFERENCES model (id), 
        FOREIGN KEY(architecture_id) REFERENCES architecture (id)
);
CREATE TABLE model_to_author (
        model_id INTEGER NOT NULL, 
        author_id INTEGER NOT NULL, 
        PRIMARY KEY (model_id, author_id), 
        FOREIGN KEY(model_id) REFERENCES model (id), 
        FOREIGN KEY(author_id) REFERENCES author (id)
);
CREATE TABLE model_to_dataset (
        model_id INTEGER NOT NULL, 
        dataset_id INTEGER NOT NULL, 
        PRIMARY KEY (model_id, dataset_id), 
        FOREIGN KEY(model_id) REFERENCES model (id), 
        FOREIGN KEY(dataset_id) REFERENCES dataset (id)
);
CREATE TABLE model_to_framework (
        model_id INTEGER NOT NULL, 
        framework_id INTEGER NOT NULL, 
        PRIMARY KEY (model_id, framework_id), 
        FOREIGN KEY(model_id) REFERENCES model (id), 
        FOREIGN KEY(framework_id) REFERENCES framework (id)
);
CREATE TABLE model_to_language (
        model_id INTEGER NOT NULL, 
        language_id INTEGER NOT NULL, 
        PRIMARY KEY (model_id, language_id), 
        FOREIGN KEY(model_id) REFERENCES model (id), 
        FOREIGN KEY(language_id) REFERENCES language (id)
);
CREATE TABLE model_to_library (
        model_id INTEGER NOT NULL, 
        library_id INTEGER NOT NULL, 
        PRIMARY KEY (model_id, library_id), 
        FOREIGN KEY(model_id) REFERENCES model (id), 
        FOREIGN KEY(library_id) REFERENCES library (id)
);
CREATE TABLE model_to_license (
        model_id INTEGER NOT NULL, 
        license_id INTEGER NOT NULL, 
        PRIMARY KEY (model_id, license_id), 
        FOREIGN KEY(model_id) REFERENCES model (id), 
        FOREIGN KEY(license_id) REFERENCES license (id)
);
CREATE TABLE model_to_paper (
        model_id INTEGER NOT NULL, 
        paper_id INTEGER NOT NULL, 
        PRIMARY KEY (model_id, paper_id), 
        FOREIGN KEY(model_id) REFERENCES model (id), 
        FOREIGN KEY(paper_id) REFERENCES paper (id)
);
CREATE TABLE model_to_tag (
        model_id INTEGER NOT NULL, 
        tag_id INTEGER NOT NULL, 
        PRIMARY KEY (model_id, tag_id), 
        FOREIGN KEY(model_id) REFERENCES model (id), 
        FOREIGN KEY(tag_id) REFERENCES tag (id)
);
CREATE TABLE discussion (
        id INTEGER NOT NULL, 
        title VARCHAR, 
        status VARCHAR, 
        num INTEGER, 
        repo_id VARCHAR, 
        repo_type VARCHAR, 
        is_pull_request INTEGER, 
        created_at VARCHAR, 
        endpoint VARCHAR, 
        target_branch VARCHAR, 
        merge_commit_oid VARCHAR, 
        diff VARCHAR, 
        model_id INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(model_id) REFERENCES model (id)
);
CREATE TABLE reuse_repo_to_issue (
        reuse_repository_id INTEGER NOT NULL, 
        github_issue_id INTEGER NOT NULL, 
        PRIMARY KEY (reuse_repository_id, github_issue_id), 
        FOREIGN KEY(reuse_repository_id) REFERENCES reuse_repository (id), 
        FOREIGN KEY(github_issue_id) REFERENCES github_issue (id)
);
CREATE TABLE reuse_file (
        id INTEGER NOT NULL, 
        path VARCHAR, 
        model_id INTEGER, 
        reuse_repository_id INTEGER, 
        PRIMARY KEY (id), 
        CONSTRAINT unique_path_model_id UNIQUE (path, model_id), 
        FOREIGN KEY(model_id) REFERENCES model (id), 
        FOREIGN KEY(reuse_repository_id) REFERENCES reuse_repository (id)
);
CREATE TABLE model_to_reuse_repository (
        model_id INTEGER NOT NULL, 
        reuse_repository_id INTEGER NOT NULL, 
        PRIMARY KEY (model_id, reuse_repository_id), 
        FOREIGN KEY(model_id) REFERENCES model (id), 
        FOREIGN KEY(reuse_repository_id) REFERENCES reuse_repository (id)
);
CREATE TABLE issue_to_assignee (
        issue_id INTEGER NOT NULL, 
        assignee_id INTEGER NOT NULL, 
        PRIMARY KEY (issue_id, assignee_id), 
        FOREIGN KEY(issue_id) REFERENCES github_issue (id), 
        FOREIGN KEY(assignee_id) REFERENCES github_user (id)
);
CREATE TABLE github_comment (
        id INTEGER NOT NULL, 
        author_id INTEGER, 
        author_association VARCHAR, 
        body VARCHAR, 
        created_at VARCHAR, 
        includes_created_edit INTEGER, 
        is_minimized INTEGER, 
        minimized_reason VARCHAR, 
        issue_id INTEGER, 
        pull_request_id INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(author_id) REFERENCES github_user (id), 
        FOREIGN KEY(issue_id) REFERENCES github_issue (id), 
        FOREIGN KEY(pull_request_id) REFERENCES github_pull_request (id)
);
CREATE TABLE github_label (
        id INTEGER NOT NULL, 
        name VARCHAR, 
        description VARCHAR, 
        color VARCHAR, 
        issue_id INTEGER, 
        pull_request_id INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(issue_id) REFERENCES github_issue (id), 
        FOREIGN KEY(pull_request_id) REFERENCES github_pull_request (id)
);
CREATE TABLE hf_commit_to_author (
        hf_commit_id INTEGER NOT NULL, 
        author_id INTEGER NOT NULL, 
        PRIMARY KEY (hf_commit_id, author_id), 
        FOREIGN KEY(hf_commit_id) REFERENCES hf_commit (id), 
        FOREIGN KEY(author_id) REFERENCES author (id)
);
CREATE TABLE hf_git_ref_to_branch (
        hf_git_ref_id INTEGER NOT NULL, 
        hf_git_ref_info_id INTEGER NOT NULL, 
        PRIMARY KEY (hf_git_ref_id, hf_git_ref_info_id), 
        FOREIGN KEY(hf_git_ref_id) REFERENCES hf_git_ref (id), 
        FOREIGN KEY(hf_git_ref_info_id) REFERENCES hf_git_ref_info (id)
);
CREATE TABLE hf_git_ref_to_tag (
        hf_git_ref_id INTEGER NOT NULL, 
        hf_git_ref_info_id INTEGER NOT NULL, 
        PRIMARY KEY (hf_git_ref_id, hf_git_ref_info_id), 
        FOREIGN KEY(hf_git_ref_id) REFERENCES hf_git_ref (id), 
        FOREIGN KEY(hf_git_ref_info_id) REFERENCES hf_git_ref_info (id)
);
CREATE TABLE discussion_to_author (
        discussion_id INTEGER NOT NULL, 
        author_id INTEGER NOT NULL, 
        PRIMARY KEY (discussion_id, author_id), 
        FOREIGN KEY(discussion_id) REFERENCES discussion (id), 
        FOREIGN KEY(author_id) REFERENCES author (id)
);
CREATE TABLE file_path (
        id INTEGER NOT NULL, 
        path VARCHAR, 
        discussion_id INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(discussion_id) REFERENCES discussion (id)
);
CREATE TABLE discussion_event (
        id INTEGER NOT NULL, 
        event_id VARCHAR, 
        type VARCHAR, 
        created_at VARCHAR, 
        author VARCHAR, 
        content VARCHAR, 
        edited INTEGER, 
        hidden INTEGER, 
        new_status VARCHAR, 
        summary VARCHAR, 
        oid VARCHAR, 
        old_title VARCHAR, 
        new_title VARCHAR, 
        discussion_id INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(discussion_id) REFERENCES discussion (id)
);
CREATE TABLE github_reaction_group (
        id INTEGER NOT NULL, 
        content VARCHAR, 
        total_count INTEGER, 
        issue_id INTEGER, 
        pull_request_id INTEGER, 
        github_comment_id INTEGER, 
        review_id INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(issue_id) REFERENCES github_issue (id), 
        FOREIGN KEY(pull_request_id) REFERENCES github_pull_request (id), 
        FOREIGN KEY(github_comment_id) REFERENCES github_comment (id), 
        FOREIGN KEY(review_id) REFERENCES github_review (id)
);