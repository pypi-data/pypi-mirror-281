import pulsectl
from prompt_toolkit.shortcuts import radiolist_dialog

def list_pulseaudio_devices():
    with pulsectl.Pulse('device-list') as pulse:
        sinks = pulse.sink_list()
        sources = pulse.source_list()
        return sinks, sources

def set_pulseaudio_sink(sink_name):
    with pulsectl.Pulse('set-default-sink') as pulse:
        for sink in pulse.sink_list():
            if sink.name == sink_name:
                pulse.default_set(sink)
                print(f"Default sink set to: {sink.description}")
                return
        print("Sink not found.")

def set_pulseaudio_source(source_name):
    with pulsectl.Pulse('set-default-source') as pulse:
        for source in pulse.source_list():
            if source.name == source_name:
                pulse.default_set(source)
                print(f"Default source set to: {source.description}")
                return
        print("Source not found.")

def main():
    sinks, sources = list_pulseaudio_devices()

    sink_choices = [(sink.name, sink.description) for sink in sinks]
    source_choices = [(source.name, source.description) for source in sources]

    device_type = radiolist_dialog(
        title="Select Device Type",
        text="Choose the device type to set as default:",
        values=[('sink', 'Sink'), ('source', 'Source')]
    ).run()

    if device_type == 'sink':
        sink_name = radiolist_dialog(
            title="Select Sink",
            text="Choose a sink to set as default:",
            values=sink_choices
        ).run()
        if sink_name:
            set_pulseaudio_sink(sink_name)
    elif device_type == 'source':
        source_name = radiolist_dialog(
            title="Select Source",
            text="Choose a source to set as default:",
            values=source_choices
        ).run()
        if source_name:
            set_pulseaudio_source(source_name)

if __name__ == "__main__":
    main()

