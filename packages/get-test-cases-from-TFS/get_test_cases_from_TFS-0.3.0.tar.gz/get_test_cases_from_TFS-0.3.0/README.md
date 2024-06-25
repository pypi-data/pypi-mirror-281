to install the Lib: 
* Excute the command **pip install get-test-cases-from-TFS==0.x.0** where x is the required version

to use the lib:
* use **create_config_from_user_data** imported from **create_config_file** method to pass the TFS project data and TFS API key, then it will create the config file and store the parameters in it(append the params to the existing file if any)
* use **featch_testcases_from_TFS** imported from **featch_testcases_from_TFS** method to get the json response of TFS as it is, including all the info
* use **fetch_test_cases_and_create_xml** imported from **communicate_TFS** to get the XML file that contains the testcases from the TFS, the cases are the ones in the test plan with the same ID which is passed in create config from user data method