from django.conf import settings
from django.contrib.staticfiles.finders import BaseFinder
from django.core.files.storage import FileSystemStorage
from django.core.checks import Error
import sass
import pathlib
import tempfile
import os

class ScssFinder(BaseFinder):
    """
    Finds .scss files specified in SCSS_ROOT and SCSS_COMPILE settings.
    """

    def __init__(self, *_args, **_kwargs):
        self.scss_compile = getattr(settings, 'SCSS_COMPILE', [])
        self.root = pathlib.Path(settings.SCSS_ROOT)
        self.css_compile_dir = pathlib.Path(getattr(settings, 'CSS_COMPILE_DIR', tempfile.gettempdir()))
        self.storage = FileSystemStorage(self.css_compile_dir)
        self.include_paths = getattr(settings, 'SCSS_INCLUDE_PATHS', None)

        self._find_matching_files()

    def check(self, **kwargs):
        """
        Checks if ScssFinder is configured correctly.

        SCSS_COMPILE should contain valid files.
        """
        errors = []

        for scss_item in self.scss_compile:
            abspath = self.root / scss_item
            if not abspath.exists() and not abspath.is_file():
                errors.append(Error(
                    f'{scss_item} is not a valid file.',
                    id='sass.E001'
                ))
        return errors

    def find(self, path, all=False):
        """
        Look for files in SCSS_ROOT, and make their paths absolute.
        """
        for (css_file, scss_file) in self.matching_files:
            if path == css_file:
                filename = str(self.css_compile_dir / path)
                self._compile_scss(css_file, scss_file)
                if os.path.exists(filename):
                    return [filename] if all else filename

    def list(self, _ignore_patterns):
        """
        Compile then list the .css files.
        """
        for (css_file, scss_file) in self.matching_files:
            yield self._compile_scss(css_file, scss_file)

    def _find_matching_files(self):
        self.matching_files = []
        for scss_item in self.scss_compile:
            abspath = self.root / scss_item
            if abspath.is_file():
                css_file = abspath.stem + '.css'
                abspath_str = str(abspath)

                self.matching_files.append(
                    (css_file, abspath_str)
                )
                
    def _compile_scss(self, css_file, scss_file):
        outpath = self.css_compile_dir / css_file
        args = {
            'filename': scss_file,
            'output_style': 'compressed',
            'include_paths': self.include_paths, 
            'source_map_contents': True
        }
        with open(outpath, 'w+') as outfile:
            outfile.write(sass.compile(**args))
        return css_file, self.storage
