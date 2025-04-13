@echo off
:: Batch script for video conversions using HandBrakeCLI
:: Requires HandBrakeCLI (Command-Line Interface version of HandBrake) to be installed and accessible via PATH.
:: Input video: MKV_HEVC_60FPS.mkv

:: Note: Not all resolutions, frame rates, formats, or codecs are supported by HandBrakeCLI.
:: Handbreak unsupported combinations will be ignored, and no output file will not be generated for them.

:: Define resolutions and frame rates for conversion
SET resolutions=720x576 720x480 1280x720 3840x2160 4096x2160
SET framerates=29.97 30.00 50.00 59.94 60.00 119.88 120.00 240.00

:: Begin processing all combinations of resolutions and frame rates
FOR %%R IN (%resolutions%) DO (
    FOR %%F IN (%framerates%) DO (
        :: Convert to MP4 with H.264 codec
        HandBrakeCLI -i Res1280x720_FPS29.97ForMP4_CODH2.64.mp4 -o %%R_%%F_MP4_H264.mp4 --width %%~R --height %%~R --rate %%~F --format av_mp4 --encoder x264

        :: Convert to MP4 with HEVC codec
        HandBrakeCLI -i Res1280x720_FPS29.97ForMP4_CODH2.64.mp4 -o %%R_%%F_MP4_HEVC.mp4 --width %%~R --height %%~R --rate %%~F --format av_mp4 --encoder x265

        :: Convert to MKV with H.264 codec
        HandBrakeCLI -i Res1280x720_FPS29.97ForMP4_CODH2.64.mp4 -o %%R_%%F_MKV_H264.mkv --width %%~R --height %%~R --rate %%~F --format av_mkv --encoder x264

        :: Convert to MKV with HEVC codec
        HandBrakeCLI -i Res1280x720_FPS29.97ForMP4_CODH2.64.mp4 -o %%R_%%F_MKV_HEVC.mkv --width %%~R --height %%~R --rate %%~F --format av_mkv --encoder x265

        :: Convert to MPEG-2
        HandBrakeCLI -i Res1280x720_FPS29.97ForMP4_CODH2.64.mp4 -o %%R_%%F_MPEG2.mpeg --width %%~R --height %%~R --rate %%~F --format mpeg --encoder mpeg2

        :: Convert to WMV
        HandBrakeCLI -i Res1280x720_FPS29.97ForMP4_CODH2.64.mp4 -o %%R_%%F_WMV.wmv --width %%~R --height %%~R --rate %%~F --format wmv --encoder wmv
    )
)

@echo All conversions are complete!
pause