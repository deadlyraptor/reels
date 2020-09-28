import requests

bacurau = 'LKTejyk9ZIA'
vivian = '424141964'

service_prompt = ('Choose\n'
                  '-------\n'
                  '1: YouTube\n'
                  '2: Vimeo\n')

service = int(input(service_prompt))


def get_thumbnail(film, url):
    r = requests.get(url)
    file_type = r.headers.get('content-type').split('/')[1]  # e.g. image/jpg
    open(f'{film}-thumbnail.{file_type}', 'wb').write(r.content)


if service == 1:
    unique_id = input('Enter the video\'s unique ID: ')
    film = input('Film name: ')
    url = f'https://img.youtube.com/vi/{unique_id}/maxresdefault.jpg'

    get_thumbnail(film, url)

    input('Press enter to exit.')

elif service == 2:
    unique_id = input('Enter the vide\'s unique ID: ')
    film = input('Film name: ')
    url = f'http://vimeo.com/api/v2/video/{unique_id}.json'

    try:
        vimeo_data = requests.get(url).json()
    except ValueError:
        pass
    else:
        thumbnail_url = vimeo_data[0]['thumbnail_large']
        get_thumbnail(film, thumbnail_url)

        input('Press enter to exit.')

else:
    print('Select the right option.')
