from .conversation import CustomConversation, MessageMetadataType


class Llama3Conversation(CustomConversation[MessageMetadataType]):

    def format(self):
        """
            random
        """
        text = ''
        text += '<|begin_of_text|>'
        for message in self.messages:
            text += f"<|start_header_id|>{str(message.role)}<|end_header_id|>\n\n{message.content}<|eot_id|>"
        text += f"<|start_header_id|>{str(self.roles.assistant)}<|end_header_id|>\n\n"
        return text

