# Klaxon Sonos Simulator

A Python-based alert tone generation system that simulates various alarm and warning tones based on the Klaxon Sonos Pulse Sounder Beacon Wall Operations Manual.

## Overview

This simulator generates audio alert tones commonly used in fire alarm systems, security systems, and emergency warning devices. It replicates the tone patterns and frequencies specified in various international standards including ISO 8201, AS1670, NEN 2575:2000, and AFNOR NF S 32 001.

## Features

- **32 Different Alert Tones**: Complete set of standardized alarm tones
- **Multiple Pattern Types**: 
  - Continuous tones
  - Alternating frequencies
  - Pulsed patterns
  - Swept frequency ranges
  - Burst patterns
- **International Standards Compliance**: Supports tones from various global standards
- **Interactive Menu System**: Easy-to-use command-line interface
- **Real-time Audio Generation**: Uses pygame for immediate audio playback
- **DIP Switch Configuration**: Visual representation of hardware switch settings

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Required Dependencies

```bash
pip install numpy pygame
```

### Clone and Run

```bash
git clone https://github.com/garethm79/klaxon-sonos-simulator.git
cd klaxon-sonos-simulator
python simulator.py
```

## Usage

Run the simulator with:

```bash
python simulator.py
```

The interactive menu will:

1. **Display All Available Tones**: Shows all 32 alert tones with descriptions, DIP switch settings, frequencies, and applicable standards
2. **Play Selected Tone**: Enter a tone number (1-32) to play the alert sound
3. **Customize Duration**: Specify playback duration in seconds (default: 5 seconds)
4. **Exit**: Enter 0 to quit the application

Simply enter the number of the tone you want to hear, optionally specify a duration, and the simulator will generate and play the corresponding alert sound.
