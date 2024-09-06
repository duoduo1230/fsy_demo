
import rv
def get_current_file_path():
    info = rv.extra_commands.sourceMetaInfoAtFrame(rv.commands.frame())
    metadata = rv.commands.sourceMediaInfo(info['node'])
    filename = metadata.get("file")
    sourceFrame = info['frame']

    files = rv.commands.existingFilesInSequence(filename)

    frames = rv.commands.existingFramesInSequence(filename)
    #rv轮回seq不一样
    if frames == [-1]:
        # return "None"
        #可能有bug
        return files[0]
    framesToFiles = dict(zip(frames, files))
    current_file_path = framesToFiles[sourceFrame]
    return current_file_path
