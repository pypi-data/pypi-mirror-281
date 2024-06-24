"""
Voicemail API
"""
import os
from io import BufferedReader
from typing import Optional, Union

from requests_toolbelt.multipart.encoder import MultipartEncoder

from .common import PersonSettingsApiChild
from ..base import ApiModel
from ..common import Greeting, VoicemailMessageStorage, StorageType, VoicemailEnabled, VoicemailNotifications, \
    VoicemailFax, VoicemailTransferToNumber, VoicemailCopyOfMessage

__all__ = ['VoicemailApi', 'VoicemailEnabledWithGreeting', 'UnansweredCalls', 'VoicemailSettings']


class VoicemailEnabledWithGreeting(VoicemailEnabled):
    """
    Voicemail enablement setting with greeting details
    """
    #: DEFAULT indicates the default greeting will be played. CUSTOM indicates a custom .wav file will be played.
    greeting: Optional[Greeting] = None
    #: Indicates a custom greeting has been uploaded.
    greeting_uploaded: Optional[bool] = None


class UnansweredCalls(VoicemailEnabledWithGreeting):
    """
    Voicemail enablement settungs for unsanswered cals
    """
    #: Number of rings before unanswered call will be sent to voicemail.
    number_of_rings: Optional[int] = None
    #: System-wide maximum number of rings allowed for number_of_rings setting.
    system_max_number_of_rings: Optional[int] = None


class VoicemailSettings(ApiModel):
    """
    User's voicemail settings
    """
    #: Voicemail is enabled or disabled.
    enabled: Optional[bool] = None
    #: Settings for sending all calls to voicemail.
    send_all_calls: Optional[VoicemailEnabled] = None
    #: Settings for sending calls to voicemail when the line is busy.
    send_busy_calls: Optional[VoicemailEnabledWithGreeting] = None
    #: Settings for sending calls to voicemail when call is unanswered
    send_unanswered_calls: Optional[UnansweredCalls] = None
    #: Settings for notifications when there are any new voicemails.
    notifications: Optional[VoicemailNotifications] = None
    #: Settings for voicemail caller to transfer to a different number by pressing zero (0).
    transfer_to_number: Optional[VoicemailTransferToNumber] = None
    #: Settings for sending a copy of new voicemail message audio via email.
    email_copy_of_message: Optional[VoicemailCopyOfMessage] = None
    #: Settings for message storage
    message_storage: Optional[VoicemailMessageStorage] = None
    #: Fax message settings
    fax_message: Optional[VoicemailFax] = None
    voice_message_forwarding_enabled: Optional[bool] = None

    @staticmethod
    def default() -> 'VoicemailSettings':
        """
        Default voicemail settings

        :return: defauilt settings
        :rtype: :class:`VoicemailSettings`
        """
        return VoicemailSettings(enabled=True,
                                 send_all_calls=VoicemailEnabled(enabled=False),
                                 send_busy_calls=VoicemailEnabledWithGreeting(enabled=False, greeting=Greeting.default),
                                 send_unanswered_calls=UnansweredCalls(enabled=True,
                                                                       greeting=Greeting.default,
                                                                       number_of_rings=3),
                                 notifications=VoicemailNotifications(enabled=False),
                                 transfer_to_number=VoicemailTransferToNumber(enabled=False),
                                 email_copy_of_message=VoicemailCopyOfMessage(enabled=False),
                                 message_storage=VoicemailMessageStorage(mwi_enabled=True,
                                                                         storage_type=StorageType.internal),
                                 fax_message=VoicemailFax(enabled=False),
                                 voice_message_forwarding_enabled=False)


class XForwardingSetting:
    pass


class VoicemailApi(PersonSettingsApiChild):
    """
    API for person's call voicemail settings
    """

    feature = 'voicemail'

    def read(self, person_id: str, org_id: str = None) -> VoicemailSettings:
        """
        Read Voicemail Settings for a Person
        Retrieve a Person's Voicemail Settings

        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via Voicemail. Voicemail audio is sent in Waveform Audio File Format, .wav, format.

        Optionally, notifications can be sent to a mobile phone via text or email. These notifications will not include
        the voicemail files.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read
        or a user auth token with spark:people_read scope can be used by a person to read their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: user's voicemail settings
        :rtype: VoicemailSettings
        """
        url = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        return VoicemailSettings.model_validate(self.get(url, params=params))

    def configure(self, person_id: str, settings: VoicemailSettings, org_id: str = None):
        """
        Configure Voicemail Settings for a Person
        Configure a person's Voicemail Settings

        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via Voicemail. Voicemail audio is sent in Waveform Audio File Format, .wav, format.

        Optionally, notifications can be sent to a mobile phone via text or email. These notifications will not
        include the voicemail files.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their settings.
        :return:
        """
        # some settings can't be part of an update
        data = settings.model_dump_json(exclude={'send_busy_calls': {'greeting_uploaded': True},
                                                 'send_unanswered_calls': {'system_max_number_of_rings': True,
                                                                           'greeting_uploaded': True},
                                                 'voice_message_forwarding_enabled': True
                                                 })
        url = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        self.put(url, data=data, params=params)

    def _configure_greeting(self, *, person_id: str, content: Union[BufferedReader, str],
                            upload_as: str = None, org_id: str = None,
                            greeting_key: str):
        """
        handled greeting configuration

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param content: the file to be uploaded, can be a path to a file or a buffered reader (opened file); if a
            reader referring to an open file is passed then make sure to open the file as binary b/c otherwise the
            content length might be calculated wrong
        :type content: Union[BufferedReader, str]
        :param upload_as: filename for the content. Only required if content is a reader; has to be a .wav file name.
        :type upload_as: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param greeting_key: 'uploadBusyGreeting' or 'uploadNoAnswerGreeting'
        """
        if isinstance(content, str):
            upload_as = os.path.basename(content)
            content = open(content, mode='rb')
            must_close = True
        else:
            must_close = False
            # an existing reader
            if not upload_as:
                raise ValueError('upload_as is required')
        encoder = MultipartEncoder({'file': (upload_as, content, 'audio/wav')})
        ep = self.f_ep(person_id=person_id, path=f'actions/{greeting_key}/invoke')
        params = org_id and {'orgId': org_id} or None
        try:
            self.post(ep, data=encoder, headers={'Content-Type': encoder.content_type},
                      params=params)
        finally:
            if must_close:
                content.close()

    def configure_busy_greeting(self, person_id: str, content: Union[BufferedReader, str],
                                upload_as: str = None, org_id: str = None):
        """
        Configure Busy Voicemail Greeting for a Person
        Configure a Person's Busy Voicemail Greeting by uploading a Waveform Audio File Format, .wav, encoded audio
        file.

        Your request will need to be a multipart/form-data request rather than JSON, using the audio/wav Content-Type.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param content: the file to be uploaded, can be a path to a file or a buffered reader (opened file); if a
            reader referring to an open file is passed then make sure to open the file as binary b/c otherwise the
            content length might be calculated wrong
        :type content: Union[BufferedReader, str]
        :param upload_as: filename for the content. Only required if content is a reader; has to be a .wav file name.
        :type upload_as: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        self._configure_greeting(person_id=person_id, content=content, upload_as=upload_as, org_id=org_id,
                                 greeting_key='uploadBusyGreeting')

    def configure_no_answer_greeting(self, person_id: str, content: Union[BufferedReader, str],
                                     upload_as: str = None, org_id: str = None):
        """
        Configure No Answer Voicemail Greeting for a Person
        Configure a Person's No Answer Voicemail Greeting by uploading a Waveform Audio File Format, .wav, encoded
        audio file.

        Your request will need to be a multipart/form-data request rather than JSON, using the audio/wav Content-Type.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param content: the file to be uploaded, can be a path to a file or a buffered reader (opened file); if a
            reader referring to an open file is passed then make sure to open the file as binary b/c otherwise the
            content length might be calculated wrong
        :type content: Union[BufferedReader, str]
        :param upload_as: filename for the content. Only required if content is a reader; has to be a .wav file name.
        :type upload_as: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        self._configure_greeting(person_id=person_id, content=content, upload_as=upload_as, org_id=org_id,
                                 greeting_key='uploadNoAnswerGreeting')

    def modify_passcode(self, person_id: str, passcode: str, org_id: str = None):
        """
        Modify a person's voicemail passcode.

        Modifying a person's voicemail passcode requires a full administrator, user administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param person_id: Modify voicemail passcode for this person.
        :type person_id: str
        :param passcode: Voicemail access passcode. The minimum length of the passcode is 6 and the maximum length is
            30.
        :type passcode: str
        :param org_id: Modify voicemail passcode for a person in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['passcode'] = passcode
        url = self.session.ep(f'telephony/config/people/{person_id}/voicemail/passcode')
        super().put(url, params=params, json=body)
