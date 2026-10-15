#let homework(
  course: "CS 439",
  semester: "Fall 2026",
  number: "X",
  author: "Matt Marsico",
  date: datetime.today(),
  doc,
) = {
  set text(font: "New Computer Modern")

  set document(
    title: course + " " + semester + " - Extended Project Proposal",
    author: author,
    date: date,
  )

  set page(
    numbering: "1",
    header: context {
      if counter(page).get().first() > 1 [
        #set text(style: "italic")
        #author - Extended Project Proposal
        #block(line(length: 100%, stroke: 0.5pt), above: 0.6em)
      ]
    },
  )

  show raw.where(block: true): it => {
    align(center,
      block(
        width: 80%,
        radius: 4pt,
        fill: luma(235),
        inset: (x: 10pt, y: 8pt),
        align(left)[
          #show raw.line: l => context {
            box(
              width: measure([#it.lines.last().count]).width,
              align(right,
                text(fill: luma(150), size: 9pt)[#l.number]
              )
            )
            h(8pt)
            text(size: 9pt, l.body)
          }
          #it
        ]
      )
    )
  }

  // header here
  align(center, {
    text(size: 16pt, weight: "bold")[#course #semester \ Extended Project Proposal]
    linebreak()
    text(size: 12pt)[#author]
    linebreak()
    emph[#date.display("[month repr:long] [day], [year]")]
    v(0.5em)
    line(length: 100%)
  })

  v(0.5em)
  doc
}

#show: homework.with(
  course: "CS 439",
  semester: "Fall 2026",
  date: datetime(year: 2026, month: 10, day: 12),
  author: "Matt Marsico"
);

#show link: set text(fill: blue)
#show link: underline
#show heading.where(level: 1): set align(center)

= Tunable Parameters of LoRa and Their Effects on Performance
== Introduction
LoRa, short for "long range", was developed in 2009 as a consumer focused long range modulation technology.
LoRa is unique not only because of its low energy, long-range communication capabilities, but also because of its
use of chirp spread spectrum (CSS) modulation. CSS utilizes the entire allocated bandwidth, making it more resilient
to channel noise. Further, CSS and LoRa have a variety of interesting properties and tunable parameters, which is what will
be explored in this project.

One of the most interesting properties of LoRa is that it can be heard below the noise floor. This is achieved by having the receiver "de-chirp"
the signal by mixing the received signal with a locally generated chirp of an opposite slope. 
This converts, what would be a frequency sweep, into a constant frequency with a sharp peak, allowing it to be easily decoded.

This robustness comes at a trade-off of a lower data rate, and is controlled by adjusting LoRa's spreading factor (SF). 
A higher spreading factor uses longer symbols which makes it easier to identify in noisy environments, but it reduces
throughput and increases airtime. According to 
#link("https://blog.semtech.com/long-range-with-lora")[Semtech's Blog Article], a LoRa with SF10 can be heard at -15 dB,
and SF12 can be heard at -20 dB. Most common LoRa radios support a spreading spectrum range of 5-12. This will be one of the more
impactful parameters that will be studied in this project, though there are still many ways to adjust the performance and characteristics 
of LoRa.

== Activities to be Performed
The goal of this project is to study and compare the effects of the different tunable parameters of LoRa on a set of metrics.

The tunable parameters will be: 
- spreading factor - range from SF6 - SF12
- bandwidth (kHz) - 7.8, 10.4, 15.6, 20.8, 31.2, 41.7, 62.5, 125, 250, 500
- cyclic coding rate - 4/5, 4/6, 4/7, 4/8
- preamble length - $>=6$, _technically a max of 65,535_
- payload size - 1-252 bytes

The measured metrics will be: _and indicated either derived/calculated or given from the board_
- packet delivery ratio - _calculated_
- RSSI (received signal strength indicator) - _given_
- SNR - _given_
- time on air - _calculated_
- goodput & throughput - _calculated_
- maximum range - _calculated / measured_

These tuning parameters will be performed across a variety of different distances, though the actual 
distances will be determined during experimentation.

== Equipment and Resources Needed
- (2) Raspberry Pi 4
- (2) Wire Antennas for Initial Development
- (2) Long Range Antennas

== Project Timeline
1. Develop communication framework and applications, allowing for the tuning and measuring of specific parameters and their effects on our metrics. Ensure that multiple successive attempts can be made to avoid outliers. (3 weeks)
2. Conduct experiments at varying distances, and organize the collected data into a matrix. (2 weeks)
3. Conduct further experiments with the goal of maximizing goodput and maximizing range. (2 weeks)
4. Create visualizations of the data to explain trends and each parameter's effect. (1 week)
5. Develop sample applications that utilize LoRa's strengths like messaging applications and collecting sensor data.
6. Develop sample applications that people are familiar with like video or audio streaming, to show the shortcomings and cons of LoRa.

== Current Project Progress (as of 10/15/26)
As of now, I have developed the communication and testing framework that will allow me to measure and derive the metrics
mentioned above, while manipulating a variety of parameters. 

To run a test, both clients will be started with the same
parameters (SF, bandwidth, coding rate, preamble length, payload size, and an expected amount of packets). Since they
may be in different locations that are far away, I have registered both Raspberry Pis onto my Tailscale network. This creates
a virtual network where I can ssh into both as if I was on the same local area network. Then, I can start the receiver program
which will start listening for packets. For each packet received, it will log the SNR, RSSI, a timestamp, and a sequence number.
This will allow me to determine which packets were lost, to later derive the packet delivery ratio. The receiver also keeps
track of when the first packet was received and when the last was received, along with the total bytes received,
so it can calculate a test run's goodput.

When a test is concluded, the receiver will write all of the per-packet information to a CSV file, and also write a
small metadata file with information (where it was done, weather conditions, etc) about the test run as well as some 
derived metrics like goodput, etc. These
can then be extracted with a script on my command and control system, in this case my laptop, where they can be further
analyzed and organized with additional scripts. 

This testing framework is complete at the time of writing this. Now, I am determining the ideal testing locations available to me, 
where I can perform more detailed and interesting test runs. My best option right now is 309 Green St which is a very tall building 
with balconies where I can place the receiver. Then, I will move around campus, noting when I do/don't have line of sight with the
receiver, as well as keeping track of distances, while performing test runs.

== Current Results
I have conducted a few test runs while developing the testing framework that help me confirm everything is working properly. 
However, these tests were conducted at an extremely short range, so they did not push the limits of LoRa, nor highlight
its long-range capabilities, but they did demonstrate an upper bound to the bandwidth I am able to get over an optimal link. 

In an indoor test where there sender and receiver had direct line of sight, and were about 20 ft apart. I was able to get about *1.2 kbps
of goodput* with the following parameters (same on the sender): 
```sh
uv run src/receiver.py \
--coding-rate 5 --spreading-factor 7 \
--bandwidth 250 --preamble-length 8 \
--num-packets 500 --payload-size 250
```

== Problems Encountered
There are a few problems and potential problems that I have encountered in pursuit of accurate empirical data.
Note that these have not been confirmed as sources of errors, though they may be in the future.

==== Antenna Reliability
Currently, I am using a simple wire that is soldered onto both LoRa boards. This works fine for close ranges and for testing, though it
may not provide the most accurate results when testing at longer range. Further it would not be representative of real-world applications
where a proper antenna would certainly be used. I have ordered real LoRa antennas so this will not be a problem for my collected data.

==== Weather Variance
If tests are conducted with a large variance in weather, for example one dry and one rainy day, there could be some error introduced into
the results. It will be important to at least keep track of the weather for each test, though the conditions may not be identical.

==== Distance Estimation
Estimating distance will be challenging since the receiver will be high above the ground, and I may be at a diagonal from the building itself.
Though I may be close in my estimation, I do not have any sort of rangefinder that would provide a scientifically accurate reading of how far
the receiver is from the sender.

== Changes in Project Plan
While the main goal of collecting real-world data and explaining the effects of different LoRa parameters has remained the same. I would like
to also explore both the theoretical and practical applications of LoRa, and create test applications that showcase this. 

For example, I could stream a video or voice over LoRa. Although it will be very slow, 
it will show exactly how slow the link speed is via the frame-rate of the video or quality of audio, and provide a useful analog to 
modern wireless and internet infrastructure.

Additionally, I would like to create some documentation so that this project is easy for novices or interested individuals to setup
and run on their own. This will be done by publishing setup information and source code to my GitHub.

== Project Deliverables
There are a variety of deliverables for this project, some are required by the rubric and others are necessary to complete my goal
of creating a valuable learning resources for individuals interested in exploring LoRa. I will summarize them below:
- Final Project Report - this will be submitted for the class and uploaded to my GitHub repository as a summary of the experiment, background information, graphs, and more.
- Sender, receiver, and browser applications - this is the core of the testing framework. The sender and receiver generate the data which will later be analyzed by the browser application where users can explore their test runs as well as generate graphs that highlight the cause and effect relationship of parameters on link properties.
- Sample applications - these will be common analogs to internet-based applications like calling, messaging, and video streaming that could be useful in understanding the capabilities of LoRa.
- Navigable graph explorer - after running a variety of tests, I'd like to create a webpage that showcases the results in a highly visual manner.
- Documentation and setup scripts - this project should be simple for users, and specifically students/novices, to setup and run on their own. This requires reproducible environments, and managing system dependencies for Debian and libraries Python, which can often be a pain point for beginners.

== Limitations of Current Approaches and Differentiating Factors
This project is unique in that it will provide real-world, easily navigable data that people can use to understand the properties of LoRa.
There are a variety of studies and projects that are available right now that allow people to test LoRa. However, by bundling LoRa applications
that act as comparisons to modern internet-based applications, and providing an easy environment to setup, this project will result in a deeper level
of learning and comprehension for users who interact with it. 

#pagebreak()
== Related Papers and References
Many of these papers are surveys, which is beneficial for understanding general characteristics of LoRa as well as how it has evolved over time.
Further, this project is similar in nature to a survey where it aims to explore many facets of LoRa, but provides real-world data to support
statements about how parameters effect key characteristics of the communication. Additionally, I have
added the paper on LoRaWAN because I would like to explain some of its workings in my presentation but I do not plan to do much experimentation with it in my project.

*A Tutorial on Chirp Spread Spectrum Modulation for LoRaWAN: Basics and Key Advances*

[1] HA H. NGUYEN EBRAHIM BEDEER ALIREZA MALEKI and ROBERT BARTON. https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10609524. ieee.org. Retrieved September 24, 2026 from https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10609524

*Long range technology for internet of things: review, challenges, and future directions*

[2] Mahmood A. Al-Shareeda, Abeer Abdullah Alsadhan, Hamzah H. Qasim, and Selvakumar Manickam. 2023. Long range technology for internet of things: review, challenges, and future directions. Bulletin EEI 12, 6 (December 2023), 3758–3767. https://doi.org/10.11591/eei.v12i6.5214

*LoRa Technology - DNA of IoT*

https://www.ijtsrd.com/papers/ijtsrd28102.pdf
[3] Ms. Helina Tandel, Ms. Anjali Gharat, and Mr. Ketan Bagade. https://www.ijtsrd.com/papers/ijtsrd28102.pdf. ijtsrd.com. Retrieved September 25, 2026 from https://www.ijtsrd.com/papers/ijtsrd28102.pdf

*Recent Advances in LoRa: A Comprehensive Survey*

[4] Zehua Sun, Huanqi Yang, Kai Liu, Zhimeng Yin, Zhenjiang Li, and Weitao Xu. 2022. Recent Advances in LoRa: A Comprehensive Survey. ACM Trans. Sensor Netw. 18, 4, Article 67 (November 2022), 44 pages. https://doi.org/10.1145/3543856

*Review Of LoRaWAN: Performance, Key Issues, And Future Perspectives*

[5] Muhammad Naim Che Kamarudin, Afida Ayob, Aini Hussain, Shaheer Ansari, Maher. G. M. Abdolrasol, and Mohamad Hanif Md Saad. 2024. Review of LoRaWAN: Performance, Key Issues and Future Perspectives. jkukm 36, 2 (March 2024), 407–418. https://doi.org/10.17576/jkukm-2024-36(2)-02

== Additional Resources
#link("https://cdn.sparkfun.com/assets/learn_tutorials/8/0/4/RFM95_96_97_98W.pdf")[RFM95W Manual]

#link("https://www.semtech.com/uploads/technology/LoRa/lora-and-lorawan.pdf")[Semtech LoRa and LoRaWAN Guide / Manual]
