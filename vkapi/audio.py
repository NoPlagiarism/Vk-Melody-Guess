from vk_api.audio import scrap_ids, TRACKS_PER_ALBUM_PAGE, TRACKS_PER_USER_PAGE, AccessDenied
from vk_api.audio import VkAudio as _VkAudio
from bs4 import BeautifulSoup

class VkAudio(_VkAudio):
    def __init__(self, vk, convert_m3u8_links=True):
        super().__init__(vk, convert_m3u8_links)

    def get_ids_iter(self, owner_id=None, album_id=None, access_hash=None):
        """ Получить список id аудиозаписей пользователя (по частям)

        :param owner_id: ID владельца (отрицательные значения для групп)
        :param album_id: ID альбома
        :param access_hash: ACCESS_HASH альбома
        """
        if owner_id is None:
            owner_id = self.user_id

        if album_id is not None:
            offset_diff = TRACKS_PER_ALBUM_PAGE
        else:
            offset_diff = TRACKS_PER_USER_PAGE

        offset = 0
        while True:
            response = self._vk.http.post(
                'https://m.vk.com/audio',
                data={
                    'act': 'load_section',
                    'owner_id': owner_id,
                    'playlist_id': album_id if album_id else -1,
                    'offset': offset,
                    'type': 'playlist',
                    'access_hash': access_hash,
                    'is_loading_all': 1
                },
                allow_redirects=False
            ).json()

            if not response['data'][0]:
                raise AccessDenied(
                    'You don\'t have permissions to browse {}\'s albums'.format(
                        owner_id
                    )
                )

            ids = scrap_ids(
                response['data'][0]['list']
            )

            if not ids:
                break

            for i in ids:
                yield i[:2]
            if response['data'][0]['hasMore']:
                offset += offset_diff
            else:
                break

    def get_ids(self, owner_id=None, album_id=None, access_hash=None):
        """ Получить список id аудиозаписей пользователя

        :param owner_id: ID владельца (отрицательные значения для групп)
        :param album_id: ID альбома
        :param access_hash: ACCESS_HASH альбома
        """
        return list(self.get_ids_iter(owner_id, album_id, access_hash))

    def get_len_user_audio(self, owner_id=None):
        if owner_id is None:
            owner_id = self.user_id

        raw_res = self._vk.http.get(f"https://vk.com/id{owner_id}")
        soup = BeautifulSoup(raw_res.text, 'html.parser')

        profile_audios = soup.find("div", id="profile_audios")

        if profile_audios is not None:
            return int(profile_audios.select('.header_count')[0].string)

        return 0
