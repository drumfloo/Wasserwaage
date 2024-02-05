<config_page>:
    orientation: 'vertical'
    padding: 10
    spacing: 10

    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: dp(50)

        Label:
            text: 'MQTT-Host'
            size_hint_x: 0.2
        TextInput:
            id: mqtt_host_input
            size_hint_x: 0.4

        Label:
            text: 'Port'
            size_hint_x: 0.1
        TextInput:
            id: port_input
            size_hint_x: 0.3
        
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: dp(50)

        Label:
            text: "User Name"
            size_hint_x: 0.2
        TextInput:
            id: username_input
            size_hint_x: 0.4

        Label:
            text: 'Password'
            size_hint_x: 0.1
        TextInput:
            id: password_input
            size_hint_x: 0.3
        
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: dp(50)

        Label:
            text: "Full Topic"
            size_hint_x: 0.2
        TextInput:
            id: full_topic_input
            size_hint_x: 0.8
    
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: dp(50)

        Label:
            text: 'Intervals'
            size_hint_x: 0.2
        Spinner:
            id: intervals_spinner
            text: "Select Interval"
            values: ["2sec","5sec","10sec"]
            size_hint_x: 0.5  # Breite des Spinners

        Label:
            text: 'Dimensions'
            size_hint_x: 0.2
        Spinner:
            id: dimensions_spinner
            text: "Select Dimension"
            values: ['1D','2D','3D']
            size_hint_x: 0.5  # Breite des Spinners

    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: dp(50)

        Button:
            text: "Check Connection"
            on_press: root.check_connection()
            size_hint_x: 0.3

        Button:
            text: 'Go'
            on_press: root.go()
            size_hint_x: 0.3

        Button:
            text: 'Back'
            on_press: root.back()
            size_hint_x: 0.4
