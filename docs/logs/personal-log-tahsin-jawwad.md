# Personal Log

[T2 Week 1 Personal Logs](#term-2-week-1)
[T2 Week 2 Personal Logs](#term-2-week-2)
[T2 Week 3 Personal Logs](#term-2-week-3)
[T2 Week 4-5 Personal Logs](#term-2-week-4-5)

[Week 3 Personal Logs](#week-3)
[Week 4 Personal Logs](#week-4)
[Week 5 Personal Logs](#week-5)
[Week 6 Personal Logs](#week-6)
[Week 7 Personal Logs](#week-7)
[Week 8 Personal Logs](#week-8)
[Week 9 Personal Logs](#week-9)
[Week 10 Personal Logs](#week-10)
[Week 11 Personal Logs](#week-11)
[Week 12 Personal Logs](#week-12)
[Week 13 Personal Logs](#week-13)
[Week 14 Personal Logs](#week-14)

## Week 3
### Date Range 
15th September 2025 - 21st September 2025

### Type of tasks worked on
![Tahsin Type of Tasks Week 3](images/tahsin-week-3.png)

### Weekly Goals
**My features**:
* The goal was to understand the project theme and contribute to the requirements document
* Created requirements document and drafted functional requirements
* Talked with other groups in class to refine our requirements

**Task from project board**:
* "Project Requirements"

**Completed/In-progress tasks**: 
* "Project Requirements"

---
## Week 4
### Date Range 
22nd September 2025 - 28th September 2025

### Type of tasks worked on
![Tahsin Type of Tasks Week 4](images/tahsin-week-4.png)

### Weekly Goals
**My features**:
* Collaborate on creating the system architecture diagram
* Collaborate on drafting and completing the project proposal

**Task from project board**:
* System Architecture Diagram
* Project Proposal

**Completed/In-progress tasks**: 
* System Architecture Diagram
* Project Proposal

## Week 5
### Date Range 
29th September 2025 - 5th October 2025

### Type of tasks worked on
![Tahsin Type of Tasks Week 5](images/tahsin-week-5.png)

### Weekly Goals
**My features**:
* Collaborated on creating Level 0 and Level 1 Data Flow Diagrams and discussion with other groups on differences in DFDs

**Task from project board**:
* Data Flow Diagram

**Completed/In-progress tasks**: 
* Data Flow Diagram (Completed)

## Week 6
### Date Range 
6th October 2025 - 12th October 2025

### Type of tasks worked on
![Tahsin Type of Tasks Week 6](images/tahsin-week-6.png)

### Weekly Goals
**My features**:
* Worked on revising the Data Flow Diagram based on the Milestone #1 requirements
* Setup tasks in the Kanban Board based on Milestone #1 requirements and assigned some people to tasks

**Task from project board**:
* DFD Revision

**Completed/In-progress tasks**: 
* DFD Revision (Completed)

## Week 7
### Date Range 
13th October 2025 - 19th October 2025

### Type of tasks worked on
![Tahsin Type of Tasks Week 7](images/tahsin-week-7.png)

### Weekly Goals
**My features**:
* Started researching on an parsing a specified zip folder using Python and useful libraries.
* Wrote initial test code to ensure that initially fails but ensures eventually that my feature works as intended.
* Implemented the parser and useful json utility and tested against the written code to ensure it works.

**Task from project board**:
* ZIP Folder Validation and Basic Parser

**Completed/In-progress tasks**: 
* ZIP Folder Validation and Basic Parser (Completed)

**Future cycle plans**:
* The next step will involve storage of the data generated from this sprint (e.g. user configs, folders structure/metadata) and possibly start looking into ways of analyzing this data.

## Week 8
### Date Range 
20th October 2025 - 26th October 2025

### Type of tasks worked on
![Tahsin Type of Tasks Week 8](images/tahsin-week-8.png)

### Weekly Goals
**My features**:
* Implemented a local code analyzer for the artifact mining system
* The analyzer performs local analysis without external APIs, supporting Python, JavaScript, Java, and C++
* Developed a test-driven approach with 24 unit tests achieving 87% code coverage
* Created working examples to demonstrate the analyzer's capabilities
* Researched on libraries and ways to extend the local code analyzer to be more general (perceval, pydriller, gitpython)

**Task from project board**:
* Local Analysis Pipeline - Code Analyzer

**Completed/In-progress tasks**: 
* Local Analysis Pipeline - Code Analyzer (Completed)

**Future cycle plans**:
- Integrate the code analyzer with git repository scanning using python libraries
- Build aggregation logic for multi-project portfolio statistics
- Storage and evaluation of the extracted contribution metrics for resume items

## Week 9
### Date Range 
27th October 2025 - 2nd November 2025

### Type of tasks worked on
![Tahsin Type of Tasks Week 9](images/tahsin-week-9.png)

### Weekly Goals
**My features**:
* Generalized and refactored the language and framework detection system into a dedicated module
* Implemented improved parsing using optional libraries (Pygments, tomllib, requirements-parser) with fallbacks
* Extended language support to 17 programming languages
* Created comprehensive test suite for new changes with 71 tests
* Integrated content-based language detection using Pygments as a fallback mechanism
* Implemented robust manifest parsing for pyproject.toml and requirements.txt
* Maintained full backward compatibility with existing code analyzer functionality

**Task from project board**:
* Identify Programming Languages and Framework

**Completed/In-progress tasks**: 
* Identify Programming Languages and Framework (Completed)

**Future cycle plans**:
- Integrate the enhanced code analyzer with git repository scanning (which can help with extracting individual contributions in collaboration projects)
- Build the aggregation layer for multi-repository portfolio analysis

## Week 10
### Date Range 
3rd November 2025 - 9th November 2025

### Type of tasks worked on
![Tahsin Type of Tasks Week 10](images/tahsin-week-10.png)

### Weekly Goals
**My features**:
* Implemented Git repository analytics with support for both PyDriller and GitPython libraries
* Created project-level analyzer to assess repository scope, collaboration patterns, and development activity
* Developed individual contributor analyzer with fuzzy author matching and detailed per-author metrics
* Built comprehensive test suite with 22 tests achieving 80-90% code coverage across modules
* Implemented activity classification system for commits (feature/bugfix/refactor/docs/test/other)
* Created week-based activity aggregation for trend analysis

**Task from project board**:
* Detect Individual/Collaboration Projects and Git Repository Analysis
* Extrapolate Individual Contributions

**Completed/In-progress tasks**: 
* Detect Individual/Collaboration Projects and Git Repository Analysis (Completed)
* Extrapolate Individual Contributions (Completed)

**Future cycle plans**:
- Wire git analytics into the main analysis pipeline
- Use database persistence for storing repository metrics
- Create visualization layer for contributor graphs and activity trends

## Week 11
### Date Range 
10th November 2025 - 16th November 2025

### Type of tasks worked on
Since there are no peer evaluations, here is a list of tasks worked on:
- Coding
- Testing my own features
- Testing other's features

### Weekly Goals
**My features**:
* Implemented canonical rank-aware ProjectInfo aggregator for merging local and git analyzer metrics
* Created unified data model with standardized fields for source identification, duration tracking, and collaboration detection
* Implemented rank-aware computation system calculating LOC, commits, skills breadth, recency, collaboration flag, and code fraction
* Built preliminary scoring formula using weighted log-scaled metrics for immediate demo capability
* Created comprehensive test suite with 11 tests achieving 75% code coverage 
* Developed CLI interface supporting local/git/merge modes with JSON input/output
* Implemented case-insensitive unions for languages/frameworks/skills with first-occurrence casing preservation
* Added extension-to-language mapping for git metrics normalization

**Task from project board**:
* Extract Key Contribution Metrics

**Completed/In-progress tasks**: 
* Extract Key Contribution Metrics (Completed)

**Future cycle plans**:
- Integrate aggregator with main pipeline to combine local and git analysis results
- Build ranking engine using rank_inputs for project significance scoring
- Implement persistence layer for storing aggregated ProjectInfo objects
- Create API endpoints for retrieving ranked project portfolios

## Week 12
### Date Range 
17th November 2025 - 23rd November 2025

### Type of tasks worked on
![Tahsin Type of Tasks Week 12](images/tahsin-week-12.png)

### Weekly Goals
**My features**:
* Implemented automatic portfolio and resume item generation for each analyzed project
* Developed PortfolioItem dataclass with structured fields: tagline, description, languages, frameworks, skills, collaboration status, and metrics
* Developed ResumeItem dataclass generating 2-3 professional bullet points tailored to individual vs. collaborative projects
* Integrated presentation generators into main pipeline orchestrator in _process_project() method
* Enhanced console output to display portfolio taglines and resume bullets in pipeline summary
* Created comprehensive test suite with 33 tests (27 unit tests, 5 integration tests, 1 demonstration test) achieving full coverage
* Implemented intelligent tagline generation distinguishing individual vs. collaborative projects with language/framework detection
* Built resume bullet generation with structured format: project scope, version control discipline, and skills application
* Added automatic list truncation (10 languages, 10 frameworks, 15 skills) to prevent overwhelming output

**Task from project board**:
* Generate Portfolio and Resume Data

**Completed/In-progress tasks**: 
* Generate Portfolio and Resume Data (Completed)

**Future cycle plans**:
- Integrate presentation items with database persistence layer for storage and retrieval
- Implement ranking/filtering system to highlight most significant projects in portfolio summaries

## Week 13
### Date Range 
24th November 2025 - 30th November 2025

### Type of tasks worked on
![Tahsin Type of Tasks Week 13](images/tahsin-week-13.png)

### Weekly Goals
**My features**:
* Enhanced portfolio and resume generation system with comprehensive metrics extraction
* Extended ProjectMetrics dataclass with additional fields: documentation metrics (doc_files, doc_words), media metrics (image_files, video_files), test metrics (test_files), and boolean flags for quick reference
* Enhanced PortfolioItem dataclass with new fields: project_type (auto-detected category), complexity (calculated level), key_features (extracted characteristics), and quality indicators (has_documentation, has_tests)
* Improved extract_project_metrics() to extract metrics from documentation analysis, categorized contents, and test files for more comprehensive data
* Improved description generation with engaging multi-sentence descriptions that mention quality indicators (tests, documentation, collaboration)
* Enhanced resume bullet generation with more action-oriented language, varied verbs, and more professional phrasing
* Added load_project_insight_by_id() method to ProjectInsightsStore for direct project lookup by database ID
* Created comprehensive test suite with 46 tests total (40 unit tests, 5 integration tests, 1 demo test) covering all new functionality
* Updated integration tests to work with improved output format while maintaining backwards compatibility

**Task from project board**:
* Generate Portfolio/Resume Item using Database #31

**Completed/In-progress tasks**: 
* Generate Portfolio/Resume Item using Database #31 (Completed)

**Future cycle plans**:
- Add export functionality for portfolio items (JSON, Markdown, HTML formats)

## Week 14
### Date Range 
1st December 2025 - 7th December 2025

### Type of tasks worked on
![Tahsin Type of Tasks Week 14](images/tahsin-week-14.png)
Also worked on creating/contributing towards Team Contract and Presentation Slides (Week 13/14)


### Weekly Goals
**My features**:
* Implemented PresentationPipeline for generating portfolio and resume items from stored project insights
* Created PresentationResult and BatchPresentationResult dataclasses for structured result handling
* Developed multiple generation methods: by project ID, by project name, by zip file, and batch generation for all projects
* Implemented list_available_projects() method to display all projects with metadata from the database
* Built comprehensive CLI interface with argparse supporting single/batch generation modes and JSON output options
* Added internal helper methods for database queries: _get_project_id(), _get_project_metadata(), _get_projects_for_zip(), _get_all_project_ids()
* Implemented error handling with graceful failure reporting for missing projects and generation failures
* Created comprehensive test suite covering all pipeline functionality: initialization, generation methods, batch processing, listing, and dataclass operations
* Achieved full test coverage for success cases, error handling, empty databases, and data serialization

**Task from project board**:
* Portfolio and Resume Generation Pipeline #166

**Completed/In-progress tasks**: 
* Portfolio and Resume Generation Pipeline #166 (Completed)

**Future cycle plans**:
- Add filtering and sorting options to generation pipeline
- Implement caching mechanism to avoid regenerating unchanged projects

## Term 2 Week 1
### Date Range 
5th January 2026 - 11th January 2026

### Type of tasks worked on
![Tahsin Type of Tasks Term 2 Week 1](images/tahsin-t2-week-1.png)

### Weekly Goals
**My features**:
* Implemented non-persistent resume item customization functionality for runtime editing of resume bullet wording
* Created apply_resume_item_customization() pure function supporting three customization modes: full bullets override, index-based edits, and project name override
* Implemented comprehensive input validation with clear error messages for all edge cases (invalid indices, empty bullets, type errors)
* Extended generate_resume_item() with optional customization parameter maintaining full backward compatibility
* Extended generate_items_from_project_id() to thread customization through to resume generation for stored projects
* Designed customization schema with clear precedence rules (bullets override > index edits > original content)
* Built whitespace handling and text normalization (strip and validate all inputs)
* Implemented max_bullets enforcement (default: 6) with configurable limit
* Created comprehensive test suite with 11 unit tests achieving 100% coverage of customization logic
* Verified all 40 existing presentation tests still pass (no breaking changes)
* Verified all 21 pipeline tests still pass (backward compatible)
* Developed working example demonstrating all customization modes
* Explicitly avoided database persistence per requirements (non-persistent, runtime-only customization)

**Task from project board**:
* Resume Item Customization #191

**Completed/In-progress tasks**: 
* Resume Item Customization #191 (Completed)

**Future cycle plans**:
- Add database schema for persisting resume customizations
- Implement persistence layer (save/load/update/delete operations)
- Create UI components for resume editing interface
- Add bulk customization operations for multiple projects

## Term 2 Week 2
### Date Range 
12th January 2026 - 18th January 2026

### Connection to Previous Week
Building on last week's resume customization feature (#191), this week focused on creating a unified CLI interface to make all pipeline functionality accessible from the command line. This provides the foundation for future UI/API development and makes the system more user-friendly for testing and demonstrations.

### Type of Tasks Worked On
![Tahsin Type of Tasks Term 2 Week 1](images/tahsin-t2-week-2.png)


**Coding Tasks:**
* Implemented unified CLI interface in `src/pipeline/cli.py`
* Created five subcommands: `analyze`, `present`, `show-portfolio`, `show-resume`, and `list`
* Developed module entry point `src/pipeline/__main__.py` enabling `python -m src.pipeline` usage
* Implemented lazy imports to avoid loading heavy dependencies at module import time
* Added comprehensive error handling with user-friendly messages and proper exit codes
* Integrated consent management (data access + LLM) with orchestrator for `analyze` command
* Built database encryption key support via environment variables
* Implemented batch operations with optional limits for `present --all` command
* Created human-readable output formatters for portfolio and resume display

**Testing Tasks:**
* Created comprehensive test suite in `tests/pipeline/test_pipeline_cli.py` 
* Wrote 11 unit tests covering all CLI subcommands and main function behavior
* Used mocking strategy to avoid heavy imports and ensure fast test execution 
* Patched PresentationPipeline and orchestrator modules at appropriate levels
* Captured stdout/stderr for output verification in formatting tests
* Verified error handling paths and exit code correctness
* Ensured no database or file system dependencies in tests
* All tests passing with 100% success rate

**Reviewing/Collaboration Tasks:**
* Cleaned up comments while preserving functionality
* Cherry-picked LOC reduction commit to `tests/cli-ui/tj` branch for clean PR workflow
* Prepared two separate PRs: one for implementation, one for tests
* Ensured backward compatibility with existing pipeline functionality

### Pull Request Reviews 
* **Add Resume Name Persistence, CLI Prompt, and Tests #202**: [Link](https://github.com/COSC-499-W2025/capstone-project-team-14/pull/202)
  - `src/pipeline/cli.py` 
  - `src/pipeline/__main__.py` 
  - `src/pipeline/cli_formatters.py` 

* This is the only PR reviewed at the time of logs. As more PRs come out, I will have reviewed more of them.

### Task from Project Board
* Initial CLI UI #204


### Completed/In-progress Tasks
* Initial CLI UI #204 (Completed)

### Goals for Next Week
* Begin work on web UI components that will consume the CLI/pipeline functionality
* Begin working on FastAPI endpoints
* Implement caching mechanism to avoid regenerating unchanged projects

### Additional Notes
* All existing tests remain passing 
* CLI provides foundation for future API/UI development
* Separation of concerns: formatting logic extracted for maintainability

## Term 2 Week 3
### Date Range 
19th January 2026 - 25th January 2026

### Connection to Previous Week
Building on last week's CLI interface (#204), this week focused on implementing project filtering functionality to help users narrow down their portfolio by tech stack. Additionally, created a comprehensive demo project to showcase all system capabilities for milestone demonstrations and peer testing.

### Type of Tasks Worked On
![Tahsin Type of Tasks Term 2 Week 3](images/tahsin-t2-week-3.png)

**Coding Tasks:**
* Enhanced `src/pipeline/cli.py` with `--language` and `--framework` filter arguments for the `list` command
* Modified `src/pipeline/presentation_pipeline.py` to implement filtering logic in `list_available_projects()` method
* Implemented case-insensitive filtering with OR logic within filter types and AND logic across filter types
* Added filter information display in CLI output headers and empty result messages
* Retrieved language/framework data from `languages_json` and `frameworks_json` database columns
* Maintained full backward compatibility (no filters returns all projects)
* Created comprehensive demo project structure in `tests/demo_capstone_project/` with 5 sub-projects
* Developed realistic demo files showcasing diverse tech stacks: Python (Django, Flask, Scikit-learn, TensorFlow), TypeScript (React Native), HTML/CSS/JavaScript, Terraform
* Compressed demo project into `tests/demo_capstone_project.zip` for pipeline testing

**Testing Tasks:**
* Created comprehensive test suite in `tests/pipeline/test_list_filtering.py`
* Wrote 15 unit and integration tests covering all filtering scenarios
* Tested single/multiple language filtering with OR logic
* Tested single/multiple framework filtering with OR logic
* Tested combined language AND framework filtering
* Verified case-insensitive matching for both filter types
* Tested empty result handling and unfiltered list behavior
* Implemented proper Windows file locking cleanup in test fixtures
* All tests passing with 100% success rate

**Other Tasks:**
* Created demo project for testing and peer feedback

### Pull Request Reviews 
* Reviewing **Data Access Consent Re-Prompt and Analyzer/Test Alignment #223**: [Link](https://github.com/COSC-499-W2025/capstone-project-team-14/pull/223)
* As more PRs come out, I will review them throughout the week

### Task from Project Board
* Project and Framework filters for Project List #225
* Create Demo Project and User Tasks for Peer Feedback #227

### Completed/In-progress Tasks
* Project and Framework filters for Project List #225 (Completed)
* Create Demo Project and User Tasks for Peer Feedback #227 (Completed)

### Goals for Next Week
* Continue work on Milestone #2 requirements
* Work on FastAPI endpoints for project management

## Term 2 Week 4-5
### Date Range 
26th January 2026 - 8th February 2026

### Connection to Previous Week
Building on last week's project filtering functionality (#225), these two weeks focused on two critical improvements: (1) implementing Git user identification to extract individual contributions from collaborative repositories, and (2) fixing a Windows ZIP path separator bug that prevented proper multi-project detection.

### Type of Tasks Worked On
![Tahsin Type of Tasks Term 2 Week 4-5](images/tahsin-t2-week-4-5.png)

**Coding Tasks:**

*Git User Identification Feature:*
* Added `git_identifier` field to `UserConfig` dataclass with automatic database migration
* Created new API endpoints in `src/api/routers/privacy.py` for setting/retrieving Git identifiers
* Enhanced `src/pipeline/orchestrator.py` to accept and process `git_identifier` parameter throughout the analysis flow
* Created `_extract_user_contribution()` helper method with case-insensitive substring matching for emails, partial emails, and names
* Integrated git_identifier flow in project upload endpoint with user-specific contribution extraction
* Implemented flexible matching supporting multiple identifier formats

*Windows ZIP Path Separator Bug Fix:*
* Fixed critical bug in `src/pipeline/orchestrator.py` where Windows-style backslash paths (`\`) in ZIP files caused improper extraction on Linux (Docker)
* Replaced `zipfile.extractall()` with custom extraction logic that normalizes path separators (converts `\` to `/`)
* Added proper directory creation with `mkdir(parents=True)` for nested structures
* Implemented filtering for directory entries and macOS metadata files (`__MACOSX`, `.` files)
* Ensured cross-platform compatibility for ZIP files created on Windows and extracted on Linux
* Bug caused detection of only 1 "root" project instead of multiple distinct projects (e.g., 5 separate projects in demo ZIP)

**Testing Tasks:**

*Git User Identification Tests (7 total):*
* Added 2 tests to `tests/config/test_config_manager.py` for database persistence and backward compatibility
* Added 1 test to `tests/api/test_privacy_consent.py` for API endpoint validation
* Created `tests/pipeline/test_git_identifier.py` with 4 tests covering email matching, partial matching, name matching, and not-found cases

*Windows ZIP Bug Fix Tests (1 new + 19 regression):*
* Added `test_zip_with_windows_style_backslash_paths` to `tests/pipeline/test_orchestrator.py` as regression test
* Test creates ZIP with Windows backslash paths and verifies multiple projects are correctly detected
* All 19 existing orchestrator tests still passing (100% backward compatibility)
* Verified with actual `tests/demo_capstone_project.zip` showing 5 projects detected instead of 1

### Pull Request Reviews 
* Will review additional PRs as they come in throughout the week

### Task from Project Board
* Git User Identification for Individual Contribution Extraction
* Windows ZIP Path Separator Bug Fix (discovered during testing)

### Completed/In-progress Tasks
* Git User Identification for Individual Contribution Extraction (Completed)
* Windows ZIP Path Separator Bug Fix (Completed)

### Goals for Next Week
* Implement frontend UI for Git identifier input during user onboarding
* Add validation and error handling for email format
* Continue work on Milestone #2 requirements
* Support multiple Git identifiers per user for different Git configurations

### Additional Notes
* Git identifier feature maintains full backward compatibility (defaults to None)
* ZIP fix ensures proper multi-project detection regardless of OS where ZIP was created
* Database migration handled automatically for existing installations
* Flexible matching algorithm supports various user input formats
* Foundation laid for future enhancements: multiple identifiers, advanced fuzzy matching, privacy options