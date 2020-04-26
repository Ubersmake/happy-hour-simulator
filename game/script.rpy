init python:
    # TODO: Display in 12H format.
    def format_time(minutes):
        return '{:02d}:{:02d}'.format(*divmod(int(minutes), 60))

init:
    $ time = 960 # Time offset from the first meeting in minutes. The first meeting starts at 04:00 PM.
    $ endtime = 1170 # Time offset from the first meeting in minutes. The last meeting ends at 07:30 PM.
    $ drunkMultiplier = 1.00 # This increases every time you drink. Affects time spent taking actions.

    # TODO: Gather points for different meetings.
    $ points = 0 # You get these for doing some things.

    $ baseTime = 10 # A base time value for all actions.

    $ fatigue = 0 # You get these for doing all things.
    $ baseFatigue = 5 # A base fatigue value for all actions.

    $ intro = True

# TODO: Meeting groups.

# Images of meeting participants and their "animations" if applicable.

image userA:
    "userA1.png"
    pause 5.0
    "userA2.png"
    pause 0.1
    "userA1.png"
    pause 3.0
    "userA2.png"
    pause 0.1
    repeat

image userB:
    "userB1.png"
    pause 4.0
    "userB2.png"
    pause 0.1
    "userB1.png"
    pause 6.5
    "userB2.png"
    pause 0.1
    repeat

image userC:
    "userC1.png"
    pause 0.1
    "userC2.png"
    pause 5.0
    "userC1.png"
    pause 2.0
    "userC2.png"
    pause 7.0
    repeat

image shiba:
    "shiba1.png"
    pause 5.0
    "shiba2.png"
    pause 0.3
    repeat

image skelly:
    "skelly1.png"
    pause 1.0
    "skelly2.png"
    pause 4.5
    "skelly1.png"
    pause 2.5
    "skelly2.png"
    pause 2.5
    repeat

image shiba1:
    "shiba1.png"
    pause 5.0
    "shiba2.png"
    pause 0.3
    repeat

image shiba2:
    "shiba1.png"
    pause 2.5
    "shiba2.png"
    pause 0.3
    "shiba1.png"
    pause 2.0
    "shiba2.png"
    pause 0.2
    repeat

image shiba3:
    "shiba1.png"
    pause 0.1
    "shiba2.png"
    pause 0.1
    repeat

image shiba4:
    "shiba1.png"
    pause 0.2
    "shiba2.png"
    pause 5.0
    repeat

image shiba5:
    "shiba1.png"
    pause 1.2
    "shiba2.png"
    pause 0.1
    "shiba1.png"
    pause 0.6
    "shiba2.png"
    pause 0.1
    "shiba1.png"
    pause 0.3
    "shiba2.png"
    pause 0.1
    repeat

image shiba6:
    "shiba1.png"
    pause 4.0
    "shiba2.png"
    pause 0.1
    repeat

# DEBUG: Used to see all variables at any point in the game.
screen debug:
    frame:
        xalign 1.0
        has vbox
        $ displayTime = format_time(time)
        text "Time: [time]"
        text "Display Time: [displayTime]"
        text "Points: [points]"
        text "Fatigue: [fatigue]"
        text "Drunk Multiplier: [drunkMultiplier]x"

# A convenient way to take actions.
label step_time(timeModifier = 0, fatigueModifier = 0):
    $ time += int((baseTime + timeModifier) * drunkMultiplier)
    $ fatigue += (baseFatigue + fatigueModifier)
    # Make sure fatigue can't go negative.
    if fatigue < 0:
        $fatigue = 0
    return

# label add_points(points, group):

# Give the player feedback based on how much fatigue they have.
# TODO: Only give each message once.
label fatigue_feedback:
    if fatigue < 20:
        pass
    elif fatigue < 30:
        "You're starting to feel a little tired."
    elif fatigue < 50:
        "You feel a little tired."
    elif fatigue < 70:
        "You're getting there."
    elif fatigue < 90:
        "You're about to pass out."
    elif fatigue < 100:
        "You really should call it a night."
    else:
        "You fool."

label populate_meeting:
    $ leftColumnX = 0.16
    $ centerColumnX = 0.50
    $ rightColumnX = 0.8425

    $ topRowY = 0.02
    $ centerRowY = 0.42

    # Row 1
    show userA:
        xalign leftColumnX
        yalign topRowY
    show userB:
        xalign centerColumnX
        yalign topRowY
    show shiba1:
        xalign rightColumnX
        yalign topRowY

    # Row 2
    show shiba3:
        xalign leftColumnX
        yalign centerRowY
    show userC:
        xalign centerColumnX
        yalign centerRowY
    show skelly:
        xalign rightColumnX
        yalign centerRowY
    return

label start:
    # TODO: Remove this and the function being called
    show screen debug

    # TODO: Rename to the background we actually want and remove "images/monitor.png"
    scene monitor

    call populate_meeting

    label intro:
        if intro:
            "Calling into the first meeting. Make sure your webcam is in its fully upright position."
            $ intro = False # TODO: Figure out why this flag is necessary to keep this thing from appearing again and again.

    label begin:
        # TODO: Start the different meetings here.
        "People are talking..."

        menu:
            "Talk about work.":
                call step_time(10)
                call work_topic

            "Talk about life.":
                call step_time(10)
                call life_topic

            "Drink":
                "You do that"
                $ drunkMultiplier += 0.1
                call step_time(5)
            
        label after_menu:
            call fatigue_feedback

    if time >= endtime:
        jump begin
    else:
        return # Ends the game.
    return

label life_topic:
    $ rand_topic = "convo_" + str(renpy.random.choice(['drink', 'pets', 'family', 'weekend', 'home', 'exercise']))
    call expression rand_topic
    return

label work_topic:
    $ rand_topic = "convo_" + str(renpy.random.choice(['week', 'cheers', 'competitor', 'quarantine', 'zoom']))
    call expression rand_topic
    return

label convo_drink:

    $added_fatigue = 0
    "What are you drinking?"

    menu:

        "I have some beers left over":
            $time += 10
            $added_fatigue = 10

        " I found some old wine.":
            "Oh, what kind of wine?"
            menu:
                "A white":
                    $time += 10
                    $added_fatigue = 10

                "A red":
                    $time += 10
                    $added_fatigue = 10

        "I need to buy more drinks soon":
            $time += 10
            $added_fatigue = 10

        "<say nothing>":
            call end_conversation
    "Gained +[added_fatigue] points of fatigue."
    $fatigue += added_fatigue
    return

label convo_family:
    $added_fatigue = 0
    "How's your family?"

    menu:
        "They're doing well":
            $time += 10
            $added_fatigue = 10

        "I haven't talked to them":
            $time += 10
            $added_fatigue = 10

        "What family?":
            $added_fatigue = 10
            call end_conversation

        "<say nothing>":
            $added_fatigue = 10
            call end_conversation

    "Gained +[added_fatigue] points of fatigue."
    $fatigue += added_fatigue
    return

label convo_pets:
    $added_fatigue = 0
    "Can I see your pet?"

    menu:
        "What pet?":
            $time += 10
            $added_fatigue += 10

        "Sure!":
            $time += 10
            $added_fatigue += 10
            call happy

        "I am the pet":
            $added_fatigue = 10
            call end_conversation

    "Gained +[added_fatigue] points of fatigue."
    $fatigue += added_fatigue
    return

label convo_week:
    $added_fatigue = 0
    "How was your week?"

    menu:
        "The week went by really quickly":
            $time += 10
            $added_fatigue += 10

        "Could have been shorter":
            $time += 10
            $added_fatigue += 10

        "It was okay":
            $time += 10
            $added_fatigue += 10

        "<say nothing>":
            $added_fatigue = 10
            call end_conversation

    "Gained +[added_fatigue] points of fatigue."
    $fatigue += added_fatigue
    return

label convo_cheers:
    $added_fatigue = 0
    "Cheers!"
    menu:
        "Raise glass and cheer":
            if fatigue > 50:
                "You spill your drink. Your pants are wet"
                $added_fatigue = 30
                $time += 30
            else:
                "You take a large sip"
                $added_fatigue = 20
        "Do nothing":
            $added_fatigue = 50

    "Gained +[added_fatigue] points of fatigue."
    $fatigue += added_fatigue
    return

label convo_weekend:
    $added_fatigue = 0
    "Any plans for the weekend?"

    menu:
        "Do some exercise":
            $time += 10
            $added_fatigue = 20
        "Wait in line at Costco":
            $time += 10
            $added_fatigue = 10
        "<Sarcastic Response>":
            $time += 10
            $added_fatigue = 5

    "Gained +[added_fatigue] points of fatigue."
    $fatigue += added_fatigue
    return

label convo_competitor:
    $added_fatigue = 0
    "Hah, how do you think Company X is doing?"

    menu:
        "I actually like using their product!":
            $time += 50
            $added_fatigue = 30
        "Let's not bring up work in this...":
            $time += 10
            $added_fatigue = 10
        "Yeah, they're terrible":
            $time += 10
            $added_fatigue = 10

    "Gained +[added_fatigue] points of fatigue."
    $fatigue += added_fatigue
    return

label convo_home:
    $added_fatigue = 0
    "How's home?"

    menu:
        "It's a mess":
            $time += 10
            $added_fatigue = 10
        "It has been claimed by my pet":
            $time += 10
            $added_fatigue = 10
        "Trying to fend off bandits":
            $time += 10
            $added_fatigue = 20

    "Gained +[added_fatigue] points of fatigue."
    $fatigue += added_fatigue
    return

label convo_exercise:
    $added_fatigue = 0
    "Did you do any exercise?"

    menu:
        "Yeah, I just paced around my room":
            $time += 10
            $added_fatigue = 15
        "Went for a short walk":
            $time += 10
            $added_fatigue = 25
        "Nope!":
            $time += 10
            $added_fatigue = 5

    "Gained +[added_fatigue] points of fatigue."
    $fatigue += added_fatigue
    return

label convo_quarantine:
    $added_fatigue = 0
    "When do you think this quarantine is over?"

    menu:
        "It will never end":
            $time += 10
            $added_fatigue = 15
        "<Optimistic response>":
            $time += 10
            $added_fatigue = 20
        "<Insert actual date>":
            $time += 10
            $added_fatigue = 25

    "Gained +[added_fatigue] points of fatigue."
    $fatigue += added_fatigue
    return

label convo_zoom:
    $added_fatigue = 0
    "Why aren't you using a Zoom Background"

    menu:
        "I think they're dumb":
            $time += 10
            $added_fatigue = 10
        "Turn off camera":
            $time += 10
            $added_fatigue = 1
        "Fine, I'll put one on...":
            $time += 10
            $added_fatigue = 30

    "Gained +[added_fatigue] points of fatigue."
    $fatigue += added_fatigue
    return

label happy:
    "Awww what a cute <insert animal>"
    return

label end_conversation:
    "Okay..."
    return
