# SPDX-FileCopyrightText: 2025 Taras Paruta (partarstu@gmail.com)
#
# SPDX-License-Identifier: Apache-2.0

from abc import ABC, abstractmethod
from typing import List

from common.models import TestExecutionResult


class TestReportingClientBase(ABC):
    @abstractmethod
    def generate_report(self, test_execution_results: List[TestExecutionResult]):
        raise NotImplementedError
