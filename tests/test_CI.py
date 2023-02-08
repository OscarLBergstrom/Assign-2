import pytest
import mail

def test_generate_build_test_message_success():  #Test for correct message with all error codes correct
    user_email = "test@gmail.com"
    commit_id = "test_commit"   
    result = [0,0,0]
    message = mail.generate_build_test_message(user_email, result,commit_id)
    content = message.get_content()
    assert message["To"] == user_email
    assert message["Subject"] == "Result from group13CI"
    assert "Test: All test passed" in content
    assert "Install: Install successfull" in content
    assert "Build: Build successfull" in content
    
    

def test_generate_build_test_message_failed(): #Tests with every step failed
    user_email = "test@gmail.com"
    commit_id = "test_commit"  
    result = [1,1,1]
    message = mail.generate_build_test_message(user_email, result,commit_id)
    content = message.get_content()
    assert message["To"] == user_email
    assert message["Subject"] == "Result from group13CI"
    #Check that extra text is not in the message
    assert "Test: All test passed" not in content
    assert "Install: Install successfull" not in content
    assert "Build: Build successfull" not in content
    #Check correct text is in the message
    assert "Test: One or more test cases failed" in content
    assert "Install: Something went wrong in the installation step" in content
    assert "Build: Something went wrong in the build step" in content
