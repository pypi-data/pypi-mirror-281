from osbot_utils.base_classes.Type_Safe import Type_Safe

from osbot_utils.helpers.Local_Caches import Local_Caches
from osbot_utils.utils.Files import path_combine

CACHE_NAME__CHATS_CACHE =  'chats_cache'


class CBR__Chats_Storage__Local(Type_Safe):
    chats_cache = Local_Caches

    def __init__(self):
        super().__init__()
        self.chats_cache.caches_name =  CACHE_NAME__CHATS_CACHE

