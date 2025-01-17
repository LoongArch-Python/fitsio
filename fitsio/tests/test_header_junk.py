import os
import tempfile
from ..fitslib import read_header


def test_header_junk():
    """
    test lenient treatment of garbage written by IDL mwrfits
    """

    data=b"""SIMPLE  =                    T /Primary Header created by MWRFITS v1.11         BITPIX  =                   16 /                                                NAXIS   =                    0 /                                                EXTEND  =                    T /Extensions may be present                       BLAT    =                    1 /integer                                         FOO     =              1.00000 /float (or double?)                              BAR@    =                  NAN /float NaN                                       BI.Z    =                  NaN /double NaN                                      BAT     =                  INF /1.0 / 0.0                                       BOO     =                 -INF /-1.0 / 0.0                                      QUAT    = '        '           /blank string                                    QUIP    = '1.0     '           /number in quotes                                QUIZ    = ' 1.0    '           /number in quotes with a leading space           QUI\xf4\x04   = 'NaN     '           /NaN in quotes                                   HIERARCH QU.@D = 'Inf     '                                                     END                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             """ # noqa

    with tempfile.TemporaryDirectory() as tmpdir:
        fname = os.path.join(tmpdir, 'test.fits')

        with open(fname, 'wb') as fobj:
            fobj.write(data)

        h = read_header(fname)
        # these keys are not hierarch but we can parse the name and then
        # leave the value as a string, so we do that.
        assert h['bar@'] == 'NAN', 'NAN garbage'
        assert h['bi.z'] == 'NaN', 'NaN garbage'
        assert h['bat'] == 'INF', 'INF garbage'
        assert h['boo'] == '-INF', '-INF garbage'
        assert h['quat'] == '', 'blank'
        assert h['quip'] == '1.0', '1.0 in quotes'
        assert h['quiz'] == ' 1.0', '1.0 in quotes'
        # the key in the header is 'QUI' + two non-ascii chars and gets
        # translated to `QUI__`
        assert h['qui__'] == 'NaN', 'NaN in quotes'
        # this key is `HIERARCH QU.@D` in the header and so gets read as is
        assert h['qu.@d'] == 'Inf', 'Inf in quotes'


def test_Header_Junk_Non_Ascii():
    data = b"SIMPLE  =                    T / file does conform to FITS standard             BITPIX  =                   16 / number of bits per data pixel                  NAXIS   =                    0 / number of data axes                            EXTEND  =                    T / FITS dataset may contain extensions            COMMENT   FITS (Flexible Image Transport System) format is defined in 'AstronomyCOMMENT   and Astrophysics', volume 376, page 359; bibcode: 2001A&A...376..359H @\x0f@\x0f \x02\x05\x18@\x02\x02\xc5@\x0c\x03\xf3@\x080\x02\x03\xbc@\x0f@@@@@@@@                                                END                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             " # noqa

    with tempfile.TemporaryDirectory() as tmpdir:
        fname = os.path.join(tmpdir, 'test.fits')
        with open(fname, 'wb') as fobj:
            fobj.write(data)

        h = read_header(fname)
        assert h["@_@_"] is None
