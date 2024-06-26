import os
import setuptools

# Открытие README.md и присвоение его long_description.
with open(os.path.join(os.path.dirname(__file__),"README.md"), "r") as fh:
	long_description = fh.read()

# Определение requests как requirements для того, чтобы этот пакет работал. Зависимости проекта.
requirements = [
	"pymysql >= 1.0",
	"psycopg2 >= 2.8",
	"numpy >= 1.20",
	"pandas >= 1.2",
	"tqdm >= 4.60",
]


# extras_require = {
# 	'windows': [
# 		'pywin32'
# 	],
# 	'linux': [
# 		'pyudev'
# 	]
# }
package_data = {
	'': ['*.md', 'database_lib/*'],
}


# Функция, которая принимает несколько аргументов. Она присваивает эти значения пакету.
setuptools.setup(
	# Имя дистрибутива пакета. Оно должно быть уникальным, поэтому добавление вашего имени пользователя в конце является обычным делом.
	name="pytopconnect",
	# Номер версии вашего пакета. Обычно используется семантическое управление версиями.
	version="1.1.1",
	# Имя автора.
	author="Apinyan Gor",
	# Его почта.
	author_email="poenixgfx102938@gmail.com",
	# Краткое описание, которое будет показано на странице PyPi.
	description="""The library is designed to interact with various databases""",
	# Длинное описание, которое будет отображаться на странице PyPi. Использует README.md репозитория для заполнения.
	long_description=long_description,
	# Определяет тип контента, используемый в long_description.
	long_description_content_type="text/markdown",
	# URL-адрес, представляющий домашнюю страницу проекта. Большинство проектов ссылаются на репозиторий.
	url="https://github.com/npawcompany/pytopconnect-1.1.x",
	# Находит все пакеты внутри проекта и объединяет их в дистрибутив.
	packages=setuptools.find_packages(),
	package_data=package_data,
	# requirements или dependencies, которые будут установлены вместе с пакетом, когда пользователь установит его через pip.
	install_requires=requirements,
	# extras_require=extras_require,
	# Предоставляет pip некоторые метаданные о пакете. Также отображается на странице PyPi.
	classifiers=[
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
		"Programming Language :: Python :: 3.10",
		"Programming Language :: Python :: 3.11",
		"Programming Language :: Python :: 3.12",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	# Требуемая версия Python.
	python_requires='>=3.6',
)