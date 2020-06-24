from distutils.core import setup, Extension
setup(name='Kuide',
      version='1.0',
      py_modules=['Gmail', 'mysmtplib', 'OpenApiSigungu','OpenApiParsing','OpenApiDo','DrawMap','Kuide','TourInformation'],
      data_files=['Resource\BasicImage.png','Resource\BookmarkButton.png','Resource\Email.png','Resource\Kuide.ico','Resource\Map.png'], requires=['telepot', 'beautifulsoup4'])