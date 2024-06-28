# -*- coding: utf-8 -*-
from uuid import uuid4
import requests
from .constants import *
from ..headers.utils import generate_headers
import logging


def uuid_generator():
    """
    Method to generate uuid
    :return: uuid
    :rtype: str
    """
    _uuid = uuid4()
    return str(_uuid)



def notification_alert(notification_type, message_status, notification_url, headers):

    """
    Calls lens-manage-console api for storing and triggering notifications

    Args:
            notification_type (string): Notebooks/AutoML/Model/Schedule
            headers (dict): headers to be passed to API
            message_status (string): Description of the notification
            notification_url (string): redirect url

    Returns:
            response after hitting the api
    """


    notification_payload = {
        "user_id": headers["X-Auth-Username"],
        "status": "Success",
        "uuid": uuid_generator(),
        "notificationURL": notification_url,
        "notificationDescription": message_status,
        "notificationType": notification_type,  # the real deal
        "createdBy": headers["X-Auth-Username"],
        "notificationDetails": {
            "senderName": headers["X-Auth-Username"],
            "accessType": "FullAccess"
        }
    }

    final_headers = {
        "X-Auth-Username": headers["X-Auth-Username"],
        "X-Project-Id": headers["X-Project-Id"],
        "X-Auth-Userid": headers["X-Auth-Userid"],
        "X-Auth-Email": headers["X-Auth-Email"]
    }

    response = requests.post(Url.notification_url, json=notification_payload, headers=final_headers)
    return response


def fetch_line_manager_details(userid, email, username, project_id):
    line_manager_email = ""
    try:
        logging.info("The username of the user is : %s", userid)
        line_manager_url = Url.LINE_MANAGER_URL + userid
        line_manager_response = requests.get(line_manager_url, headers=generate_headers(userid, email, username, project_id))
        if line_manager_response.status_code == 200:
            line_manager_response_json = line_manager_response.json()
            logging.info(line_manager_response_json)
            line_manager_email = line_manager_response_json["lineManagerDetails"]["emailId"]
            logging.info("Line manager email id : %s", line_manager_email)
        elif line_manager_response.status_code == 404:
            logging.info("Line Manager Details are unavailable")
        else:
            logging.error("Unknown Error while fetching Line-Manager Info : %s", line_manager_response.text)

        return line_manager_email

    except Exception as ex:
        logging.exception(ex)
        return line_manager_email
