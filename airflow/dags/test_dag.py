# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""
Example DAG for demonstrating behavior of Datasets feature.

Notes on usage:

Turn on all the dags.

DAG dataset_produces_1 should run because it's on a schedule.

After dataset_produces_1 runs, dataset_consumes_1 should be triggered immediately
because its only dataset dependency is managed by dataset_produces_1.

No other dags should be triggered.  Note that even though dataset_consumes_1_and_2 depends on
the dataset in dataset_produces_1, it will not be triggered until dataset_produces_2 runs
(and dataset_produces_2 is left with no schedule so that we can trigger it manually).

Next, trigger dataset_produces_2.  After dataset_produces_2 finishes,
dataset_consumes_1_and_2 should run.

Dags dataset_consumes_1_never_scheduled and dataset_consumes_unknown_never_scheduled should not run because
they depend on datasets that never get updated.
"""
from __future__ import annotations

import pendulum

from airflow import DAG, Dataset
from airflow.operators.bash import BashOperator

# [START dataset_def]
dag1_dataset = Dataset('s3://dag1/output_1.txt', extra={'hi': 'bye'})
# [END dataset_def]
dag2_dataset = Dataset('s3://dag2/output_1.txt', extra={'hi': 'bye'})

with DAG(
    dag_id='test_dag_bart',
    catchup=False,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule='@daily',
    tags=['produces', 'dataset-scheduled'],
) as dag1:
    # [START task_outlet]
    BashOperator(outlets=[dag1_dataset], task_id='producing_task_1', bash_command="sleep 5")
    # [END task_outlet]
