# -*- coding: utf-8 -*-

"""
A simple regex parser to parse conventional commit message.

Usage example::

    import fixa.conventional_commits as conv_commits

    conv_commits.tokenize
    conv_commits.ConventionalCommit
    conv_commits.ConventionalCommitParser
    conv_commits.SemanticCommitEnum
    conv_commits.default_parser
    conv_commits.is_certain_semantic_commit
    conv_commits.is_feat_commit
    conv_commits.is_fix_commit
    conv_commits.is_test_commit
    conv_commits.is_utest_commit
    conv_commits.is_itest_commit
    conv_commits.is_ltest_commit
    conv_commits.is_doc_commit
    conv_commits.is_build_commit
    conv_commits.is_publish_commit
    conv_commits.is_release_commit

Reference:

- Conventional Commits: https://www.conventionalcommits.org/en/v1.0.0/
"""

import typing as T
import re
import enum
import string
import dataclasses

__version__ = "0.1.1"

DELIMITERS = "!@#$%^&*()_+-=~`[{]}\\|;:'\",<.>/? \t\n"
CHARSET = string.ascii_letters


def tokenize(
    text: str,
    delimiters: str = DELIMITERS,
) -> T.List[str]:
    """
    Example:

        >>> tokenize("a, b (c): d - e")
        ["a", "b", "c", "d", "e"]
    """
    cleaner_text = text
    for delimiter in delimiters:
        cleaner_text = cleaner_text.replace(delimiter, " ")
    words = [word.strip() for word in cleaner_text.split(" ") if word.strip()]
    return words


def _get_subject_regex(_types: T.List[str]) -> T.Pattern:
    """
    Example: ``${type}(${scope})${breaking}: ${description}``
    """
    return re.compile(
        rf"^(?P<types>[\w ,]+)(?:\((?P<scope>[\w-]+)\))?(?P<breaking>!)?:[ \t]?(?P<description>.+)$"
    )


@dataclasses.dataclass
class ConventionalCommit:
    """
    Data container class for conventional commits message.
    """

    types: T.List[str]
    description: str = None
    scope: T.Optional[str] = None
    breaking: T.Optional[str] = None

    def render(self) -> str:
        """
        Render the conventional commit message.
        """
        types = ", ".join(self.types)
        scope = f"({self.scope})" if self.scope else ""
        breaking = "!" if self.breaking else ""
        description = self.description if self.description else ""
        return f"{types}{scope}{breaking}: {description}"


class ConventionalCommitParser:
    """
    The customizable parser class. It tries to parse from
    ``type1, type2 (scope): {description}

    Usage example:

        >>> parser = ConventionalCommitParser(types=["feat", "fix", "build"])
        >>> parser.parse_message("feat, build(STORY-001): add validator")
        ConventionalCommit(types=['feat', 'build'], description='add validator', scope='STORY-001', breaking=None)

    :param types: the list of conventional commit type you want to monitor
    """

    def __init__(self, types: T.List[str]):
        self.types = [type_.lower().strip() for type_ in types]
        self.subject_regex = _get_subject_regex(types)

    def extract_subject(self, msg: str) -> str:
        """
        Extract the subject line.

        >>> ConventionalCommitParser().extract_subject("feat, build(STORY-001): add validator\\nWe have done the following")
        'feat, build(STORY-001): add validator'
        """
        return msg.split("\n")[0].strip()

    def extract_commit(self, subject: str) -> ConventionalCommit:
        """
        Extract conventional commit object from the subject.
        """
        match = self.subject_regex.match(subject)
        types = [
            word.strip()
            for word in match["types"].split(",")
            if word.strip() in self.types
        ]

        # Debug only
        # print(match)
        # print([match["types"],])
        # print([match["description"], ])
        # print([match["scope"], ])
        # print([match["breaking"], ])

        return ConventionalCommit(
            types=types,
            description=match["description"],
            scope=match["scope"],
            breaking=match["breaking"],
        )

    def parse_message(self, commit_message: str) -> T.Optional[ConventionalCommit]:
        """
        Parse the commit message, return None if it is not a conventional commit.
        """
        try:
            return self.extract_commit(self.extract_subject(commit_message))
        except Exception as e:
            return None


class SemanticCommitEnum(str, enum.Enum):
    """
    Semantic commit message can help CI to determine what you want to do.

    It is a good way to allow developer controls the CI behavior with small
    effort.
    """

    # based on purpose
    chore = "chore"  # house cleaning, do nothing
    feat = "feat"  # new feature
    feature = "feature"  # new feature
    fix = "fix"  # fix something
    doc = "doc"  # documentation
    test = "test"  # run all test
    utest = "utest"  # run unit test
    itest = "itest"  # run integration test
    ltest = "ltest"  # run load test
    build = "build"  # build artifacts
    pub = "pub"  # publish artifacts
    publish = "publish"  # publish artifacts
    rls = "rls"  # release
    release = "release"  # release
    clean = "clean"  # cleanup
    cleanup = "cleanup"  # cleanup

    # based on environment
    dev = "dev"
    develop = "develop"
    # test = "test" # already have above
    int = "int"
    stage = "stage"
    staging = "staging"
    qa = "qa"
    preprod = "preprod"
    prod = "prod"
    blue = "blue"
    green = "green"


default_parser = ConventionalCommitParser(types=list(SemanticCommitEnum))


def is_certain_semantic_commit(
    commit_message: str,
    stub: T.Union[str, T.List[str]],
    parser: ConventionalCommitParser = default_parser,
) -> bool:
    """
    Identify whether the commit message is certain type of semantic commit.

    Below is an example to check if the commit message has the keyword "fix"::

        >>> is_certain_semantic_commit(
        ...     commit_message="fix: the function cannot handle this edge case",
        ...     stub="fix",
        ... )
        True

    :param commit_message: the commit message.
    :param stub: commit type stub or list of commit type stub.
    :param parser: a :class:`ConventionalCommitParser` object.

    :return: a boolean value
    """
    commit = parser.parse_message(commit_message)
    if commit is None:  # pragma: no cover
        return False
    if isinstance(stub, str):
        stub_set = {
            stub,
        }
    else:
        stub_set = set(stub)
    return len(set(commit.types).intersection(stub_set)) > 0


def is_feat_commit(commit_message: str) -> bool:
    return is_certain_semantic_commit(
        commit_message,
        [SemanticCommitEnum.feat, SemanticCommitEnum.feature],
    )


def is_fix_commit(commit_message: str) -> bool:
    return is_certain_semantic_commit(
        commit_message,
        SemanticCommitEnum.fix,
    )


def is_test_commit(commit_message: str) -> bool:
    return is_certain_semantic_commit(
        commit_message,
        [
            SemanticCommitEnum.test,
            SemanticCommitEnum.utest,
            SemanticCommitEnum.itest,
            SemanticCommitEnum.ltest,
        ],
    )


def is_utest_commit(commit_message: str) -> bool:  # pragma: no cover
    return is_certain_semantic_commit(
        commit_message,
        SemanticCommitEnum.utest,
    )


def is_itest_commit(commit_message: str) -> bool:  # pragma: no cover
    return is_certain_semantic_commit(
        commit_message,
        SemanticCommitEnum.itest,
    )


def is_ltest_commit(commit_message: str) -> bool:  # pragma: no cover
    return is_certain_semantic_commit(
        commit_message,
        SemanticCommitEnum.ltest,
    )


def is_doc_commit(commit_message: str) -> bool:  # pragma: no cover
    return is_certain_semantic_commit(
        commit_message,
        SemanticCommitEnum.doc,
    )


def is_build_commit(commit_message: str) -> bool:
    return is_certain_semantic_commit(
        commit_message,
        SemanticCommitEnum.build,
    )


def is_publish_commit(commit_message: str) -> bool:  # pragma: no cover
    return is_certain_semantic_commit(
        commit_message,
        [SemanticCommitEnum.pub, SemanticCommitEnum.publish],
    )


def is_release_commit(commit_message: str) -> bool:  # pragma: no cover
    return is_certain_semantic_commit(
        commit_message,
        [SemanticCommitEnum.rls, SemanticCommitEnum.release],
    )
