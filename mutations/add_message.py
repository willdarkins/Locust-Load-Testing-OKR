ADD_MESSAGE_TO_CONVERSATIONS = """
mutation AddMessageToConversations($input: AddMessageToConversationsInput!) {
    addMessageToConversations(input: $input) {
        ...Message
        __typename
    }
}

fragment Message on MessageType {
    author {
        ...MessageAuthor
        __typename
    }
    authorEmail
    authorId
    body
    bodyPlainText
    created
    fileIds
    files {
        ...File
        __typename
    }
    id
    isInternal
    title
    __typename
}

fragment MessageAuthor on User {
    id
    fullName
    __typename
}

fragment File on File {
    ...DownloadFile
    filename
    fileExtension
    status
    __typename
}

fragment DownloadFile on File {
    id
    downloadUri(expiryTimeInSecs: 86400) {
        ...SignedURI
        __typename
    }
    __typename
}

fragment SignedURI on SignedURI {
    expiresAt
    uri
    __typename
}
"""


def add_message_variables(conversation_id: int, message_body: str, is_internal: bool = False):
    """
    Helper function to generate variables for AddMessageToConversations mutation
    
    Args:
        conversation_id: ID of the conversation to add message to
        message_body: Plain text content of the message (defaults to "test")
        is_internal: Whether the message is internal (defaults to False)
    
    Returns:
        dict: Variables object ready for the mutation
    """
    return {
        "input": {
            "messages": [
                {
                    "body": f"<p>{message_body}</p>",
                    "bodyPlainText": message_body,
                    "conversationId": conversation_id,
                    "fileIds": [],
                    "isInternal": is_internal,
                    "notificationData": {}
                }
            ]
        }
    }