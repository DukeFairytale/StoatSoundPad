import asyncio

class SoundManager:
    def __init__(self):
        self.active_sounds = {}

    async def _play_sound(self, user_id, sound_id):
        try:
            print(f'START {user_id}: {sound_id}')
            await asyncio.sleep(5)
            print(f'END {user_id}: {sound_id}')
        except asyncio.CancelledError:
            print(f'CANCELLED {user_id}: {sound_id}')
            raise


    async def play(self, user_id, sound_id):
        key = (user_id, sound_id)

        if key in self.active_sounds:
            self.active_sounds[key].cancel()

        task = asyncio.create_task(self._play_sound(user_id, sound_id))

        self.active_sounds[key] = task

        def on_done(finished_task):
            if self.active_sounds.get(key) is finished_task:
                del self.active_sounds[key]

        task.add_done_callback(on_done)



