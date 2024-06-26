import sys
import os
import pytest

from yaml_config_day.config_manager import ProjectConfigManager


# I am not sure how much effort to put into mocking the xcures API endpoints, so this is a perfuncotry test to exercise at least some of the code.
def test_fail_to_find_yaml_file():

        xcures_env = os.getenv('XCURES_ENV', 'n/a')
        # We are testing the case of failing to find the yaml file, so will override the env var with a non-existent env
        xcures_env = "not_a_real_env"
         
        success = False
        try:
            config = ProjectConfigManager("xcures", xcures_env).get_config()
            success = True
        except Exception as e:
            assert str(e).__contains__("The expected yaml config file has not been detected in the expected location:") == True

        assert success == False
        #base_url = config['base_url']
        #base_auth_url = config['base_auth_url']
        #project_id = config['project_id']
        #client_id = config['client_id']
        #client_secret = config['client_secret']

