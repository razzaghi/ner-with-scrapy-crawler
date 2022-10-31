import json
import re


def mailtext2json(mailtext):
    cleanedtext = cleanmailtext(mailtext)
    json_message = json.dumps(parsejsonrepmessage(cleanedtext.encode('utf-8', errors='ignore').decode('utf-8')))
    return json_message


def cleanmailtext(mailtext):
    cleanedtext = removeheadhtmltag(mailtext)
    cleanedtext = cleanhtml(cleanedtext)
    cleanedtext = removelinks(cleanedtext)
    cleanedtext = removedoblewhitespaces(cleanedtext)
    cleanedtext = removemultiplelinebreaks(cleanedtext)
    return cleanedtext.rstrip()


def cleanhtml(raw_html):
    CLEANR = re.compile(r'<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub('</p>', "</p>\n", raw_html)
    cleantext = re.sub('<br\s?\/>|<br>', "\n", cleantext)
    cleantext = re.sub(CLEANR, '', cleantext)
    return cleantext


def removelinks(text):
    CLEANR = re.compile(r'\[(http.*?)\]')
    return re.sub(CLEANR, '', text)


def removemultiplelinebreaks(text):
    CLEANR = re.compile(r'[\r\n]{3,}')
    return re.sub(CLEANR, r'\n\n', text)


def removedoblewhitespaces(text):
    CLEANR = re.compile(r'[^\S\r\n]{2,}')
    return re.sub(CLEANR, ' ', text)


def removeheadhtmltag(text):
    CLEANR = re.compile(r'<head>(?:.|\n|\r)+?<\/head>')
    return re.sub(CLEANR, '', text)


def cleanhtmlcomment(raw_html):
    CLEANR = re.compile(r'<!--.*|\r|\n-->')
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext

def parsejsonrepmessage(message_text):
    parsed_message = json.loads(json.dumps({"data": {"body": message_text}}))
    return parsed_message
