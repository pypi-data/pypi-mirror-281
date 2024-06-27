import requests
import os

# detect the running OS and return the appropriate file path delimiter
def get_path_delimiter():
    """
    Detect the running OS and return the appropriate file path delimiter.
    """
    return '\\' if os.name == 'nt' else '/'


# SEND MESSAGE TO TELEGRAM
def telegram_send_photo(token_key, chat_id, message, file_path):
    """
    Send a photo to a Telegram group.

    Args:
        token_key (str): Telegram token key.
        chat_id (str): ID of the target Telegram channel/group, e.g., '-1001439492355'.
        message (str): Your text message.
        file_path (str): Path of the file/photo to send via Telegram.

    Returns:
        object: Response object from the Telegram API.
    """
    file_name = file_path.split(get_path_delimiter())[-1]
    file_type = file_name.split('.')[-1]
    files = [('photo', (file_name, open(file_path, 'rb'), 'image/{}'.format(file_type)))]
    url = 'https://api.telegram.org/bot{}/sendPhoto'.format(token_key)
    payload = {'chat_id': chat_id, 'caption': message}
    response = requests.post(url, headers={}, data=payload, files=files)
    return response

def telegram_send_message(token_key, chat_id, message):
	"""
	Send a message to a Telegram group.

	Args:
		token_key (str): Telegram token key.
		chat_id (str): ID of the target Telegram channel/group, e.g., '-1001439492355'.
		message (str): Your text message.

	Returns:
		object: Response object from the Telegram API.
	"""
	tel_url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(token_key, chat_id, message) # thêm chữ bot trước token so với code cũ
	response = requests.post(tel_url)
	return response.json()