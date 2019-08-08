# -*- coding: utf-8 -*- #
# Copyright 2019 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Implements command to cancel a given active OS patch job."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.compute.os_config import osconfig_utils
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.compute.os_config import resource_args
from googlecloudsdk.core import properties


@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class Cancel(base.Command):
  """Cancel the given active OS patch job.

  ## EXAMPLES

  To cancel the patch job 'job1', run:

        $ {command} job1

  """

  @staticmethod
  def Args(parser):
    resource_args.AddPatchJobResourceArg(parser, 'to cancel.')

  def Run(self, args):
    project = properties.VALUES.core.project.GetOrFail()
    patch_job_ref = args.CONCEPTS.patch_job.Parse()

    release_track = self.ReleaseTrack()
    # TODO(b/133780270): Migrate to v1alpha2.
    api_version = 'v1alpha1'
    client = osconfig_utils.GetClientInstance(
        release_track, api_version_override=api_version)
    messages = osconfig_utils.GetClientMessages(
        release_track, api_version_override=api_version)

    request = messages.OsconfigProjectsPatchJobsCancelRequest(
        cancelPatchJobRequest=None,
        name=osconfig_utils.GetPatchJobUriPath(project, patch_job_ref.Name()))
    return client.projects_patchJobs.Cancel(request)
