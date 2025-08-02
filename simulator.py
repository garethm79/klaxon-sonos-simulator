"""
Klaxon Sonos Simulator - Alert Tone Generation System
Data from Texecom Sonos Pulse Sounder Beacon Wall Operations Manual
"""

import numpy as np
import pygame
import time
import re
from typing import Optional, List, Tuple

class AlertToneLookup:
    def __init__(self):
        # Define the tone data with all configurations
        self.tones = {
            1: {
                'frequency': '970Hz',
                'description': '970Hz',
                'dip_switches': 'O-O-O-O-O',
                'pattern': 'continuous',
                'standard': None
            },
            2: {
                'frequency': '800Hz/970Hz @ 2Hz',
                'description': '800Hz/970Hz @ 2Hz',
                'dip_switches': 'O-O-O-O-I',
                'pattern': 'alternating',
                'standard': None
            },
            3: {
                'frequency': '800Hz – 970Hz @ 1Hz',
                'description': '800Hz – 970Hz @ 1Hz',
                'dip_switches': 'O-O-O-I-O',
                'pattern': 'alternating',
                'standard': None
            },
            4: {
                'frequency': '970Hz',
                'description': '970Hz 1s OFF/1s ON',
                'dip_switches': 'O-O-O-I-I',
                'pattern': 'pulsed',
                'standard': None
            },
            5: {
                'frequency': '970Hz/630Hz',
                'description': '970Hz, 0.5s/ 630Hz, 0.5s',
                'dip_switches': 'O-O-I-O-O',
                'pattern': 'alternating',
                'standard': None
            },
            6: {
                'frequency': '554Hz/440Hz',
                'description': '554Hz, 0.1s/ 440Hz, 0.4s',
                'dip_switches': 'O-O-I-O-I',
                'pattern': 'alternating',
                'standard': 'AFNOR NF S 32 001'
            },
            7: {
                'frequency': '500 – 1200Hz',
                'description': '500 – 1200Hz, 3.5s/ 0.5s OFF (NEN 2575:2000 Dutch Slow Whoop)',
                'dip_switches': 'O-O-I-I-O',
                'pattern': 'swept',
                'standard': 'NEN 2575:2000'
            },
            8: {
                'frequency': '420Hz',
                'description': '420Hz 0.6s ON/0.6s OFF (Australia AS1670 Alert tone)',
                'dip_switches': 'O-O-I-I-I',
                'pattern': 'pulsed',
                'standard': 'AS1670'
            },
            9: {
                'frequency': '1000 - 2500Hz',
                'description': '1000 - 2500Hz, 0.5s/ 0.5s OFF x 3/1.5s OFF ( AS1670 Evacuation)',
                'dip_switches': 'O-I-O-O-O',
                'pattern': 'swept_burst',
                'standard': 'AS1670'
            },
            10: {
                'frequency': '550Hz/440Hz @ 0.5Hz',
                'description': '550Hz/440Hz @ 0.5Hz',
                'dip_switches': 'O-I-O-O-I',
                'pattern': 'alternating',
                'standard': None
            },
            11: {
                'frequency': '970Hz',
                'description': '970Hz, 0.5s ON/0.5s OFF x 3/ 1.5s OFF',
                'dip_switches': 'O-I-O-I-O',
                'pattern': 'pulsed_burst',
                'standard': 'ISO 8201'
            },
            12: {
                'frequency': '2850Hz',
                'description': '2850Hz, 0.5s ON/0.5s OFF x 3/1.5s OFF',
                'dip_switches': 'O-I-O-I-I',
                'pattern': 'pulsed_burst',
                'standard': 'ISO 8201'
            },
            13: {
                'frequency': '1200Hz – 500Hz @ 1Hz',
                'description': '1200Hz – 500Hz @ 1Hz',
                'dip_switches': 'O-I-I-O-O',
                'pattern': 'swept',
                'standard': 'DIN 33 404'
            },
            14: {
                'frequency': '400Hz',
                'description': '400Hz',
                'dip_switches': 'O-I-I-O-I',
                'pattern': 'continuous',
                'standard': None
            },
            15: {
                'frequency': '550Hz/1000Hz',
                'description': '550Hz, 0.7s/1000Hz, 0.33s',
                'dip_switches': 'O-I-I-I-O',
                'pattern': 'alternating',
                'standard': None
            },
            16: {
                'frequency': '1500Hz – 2700Hz @ 3Hz',
                'description': '1500Hz – 2700Hz @ 3Hz',
                'dip_switches': 'O-I-I-I-I',
                'pattern': 'swept',
                'standard': None
            },
            17: {
                'frequency': '750Hz',
                'description': '750Hz',
                'dip_switches': 'I-O-O-O-O',
                'pattern': 'continuous',
                'standard': None
            },
            18: {
                'frequency': '2400Hz',
                'description': '2400Hz',
                'dip_switches': 'I-O-O-O-I',
                'pattern': 'continuous',
                'standard': None
            },
            19: {
                'frequency': '660Hz',
                'description': '660Hz',
                'dip_switches': 'I-O-O-I-O',
                'pattern': 'continuous',
                'standard': None
            },
            20: {
                'frequency': '660Hz',
                'description': '660Hz 1.8s ON/1.8s OFF',
                'dip_switches': 'I-O-O-I-I',
                'pattern': 'pulsed',
                'standard': None
            },
            21: {
                'frequency': '660Hz',
                'description': '660Hz 0.15s ON/0.15s OFF',
                'dip_switches': 'I-O-I-O-O',
                'pattern': 'pulsed',
                'standard': None
            },
            22: {
                'frequency': '510Hz/610Hz',
                'description': '510Hz, 0.25s/ 610Hz, 0.25s',
                'dip_switches': 'I-O-I-O-I',
                'pattern': 'alternating',
                'standard': None
            },
            23: {
                'frequency': '800/1000Hz',
                'description': '800/1000Hz 0.5s each (1Hz)',
                'dip_switches': 'I-O-I-I-O',
                'pattern': 'alternating',
                'standard': None
            },
            24: {
                'frequency': '250Hz – 1200Hz @ 12Hz',
                'description': '250Hz – 1200Hz @ 12Hz',
                'dip_switches': 'I-O-I-I-I',
                'pattern': 'swept',
                'standard': None
            },
            25: {
                'frequency': '500Hz – 1200Hz @ 0.33Hz',
                'description': '500Hz – 1200Hz @ 0.33Hz',
                'dip_switches': 'I-I-O-O-O',
                'pattern': 'swept',
                'standard': None
            },
            26: {
                'frequency': '2400Hz – 2900Hz @ 9Hz',
                'description': '2400Hz – 2900Hz @ 9Hz',
                'dip_switches': 'I-I-O-O-I',
                'pattern': 'swept',
                'standard': None
            },
            27: {
                'frequency': '2400Hz – 2900Hz @ 3Hz',
                'description': '2400Hz – 2900Hz @ 3Hz',
                'dip_switches': 'I-I-O-I-O',
                'pattern': 'swept',
                'standard': None
            },
            28: {
                'frequency': '500 - 1200Hz',
                'description': '500 - 1200Hz, 0.5s/ 0.5s OFF x 3/1.5s OFF ( AS1670 Evacuation)',
                'dip_switches': 'I-I-O-I-I',
                'pattern': 'swept_burst',
                'standard': 'AS1670'
            },
            29: {
                'frequency': '800Hz – 970Hz @ 9Hz',
                'description': '800Hz – 970Hz @ 9Hz',
                'dip_switches': 'I-I-I-O-O',
                'pattern': 'swept',
                'standard': None
            },
            30: {
                'frequency': '800Hz – 970Hz @ 3Hz',
                'description': '800Hz – 970Hz @ 3Hz',
                'dip_switches': 'I-I-I-O-I',
                'pattern': 'swept',
                'standard': None
            },
            31: {
                'frequency': '800Hz',
                'description': '800Hz, 0.25s ON/1s OFF',
                'dip_switches': 'I-I-I-I-O',
                'pattern': 'pulsed',
                'standard': None
            },
            32: {
                'frequency': '500Hz – 1200Hz',
                'description': '500Hz – 1200Hz, 3.75s/0.25s OFF',
                'dip_switches': 'I-I-I-I-I',
                'pattern': 'swept',
                'standard': 'AS2220'
            }
        }
    
    def get_tone_by_number(self, tone_number):
        """Get tone information by tone number"""
        return self.tones.get(tone_number)
    
    def search_by_standard(self, standard):
        """Find all tones matching a specific standard"""
        results = []
        for tone_num, data in self.tones.items():
            if data['standard'] and standard.upper() in data['standard'].upper():
                results.append({'tone_number': tone_num, **data})
        return results
    
    def search_by_frequency(self, frequency):
        """Find tones containing a specific frequency"""
        results = []
        for tone_num, data in self.tones.items():
            if str(frequency) in data['frequency']:
                results.append({'tone_number': tone_num, **data})
        return results
    
    def search_by_pattern(self, pattern):
        """Find tones by pattern type (continuous, pulsed, alternating, swept, etc.)"""
        results = []
        for tone_num, data in self.tones.items():
            if pattern.lower() in data['pattern'].lower():
                results.append({'tone_number': tone_num, **data})
        return results
    
    def search_by_description(self, search_term):
        """Search tone descriptions for a specific term"""
        results = []
        for tone_num, data in self.tones.items():
            if search_term.lower() in data['description'].lower():
                results.append({'tone_number': tone_num, **data})
        return results
    
    def get_dip_switch_config(self, tone_number):
        """Get DIP switch configuration for a tone number"""
        tone = self.get_tone_by_number(tone_number)
        if tone:
            return tone['dip_switches']
        return None
    
    def find_tone_by_dip_switches(self, dip_config):
        """Find tone number by DIP switch configuration"""
        for tone_num, data in self.tones.items():
            if data['dip_switches'] == dip_config:
                return {'tone_number': tone_num, **data}
        return None
    
    def list_all_standards(self):
        """Get list of all available standards"""
        standards = set()
        for data in self.tones.values():
            if data['standard']:
                standards.add(data['standard'])
        return sorted(list(standards))
    
    def get_evacuation_tones(self):
        """Get all evacuation-related tones"""
        return self.search_by_description('evacuation')
    
    def get_alert_tones(self):
        """Get all alert-related tones"""
        return self.search_by_description('alert')


class ToneGenerator:
    """Generate and play audio tones based on the alert tone specifications"""
    
    # Common pattern durations
    BURST_PATTERN_DURATION = 2.5  # 3*(0.5) + 1.5 = 2.5s (actual pattern duration)
    BURST_CYCLE_DURATION = 4.5    # Total cycle including gap calculation compatibility
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        
        # Initialize pygame mixer for audio playback
        try:
            import pygame
            pygame.mixer.init(frequency=sample_rate, size=-16, channels=2, buffer=1024)
            self.pygame_available = True
        except ImportError:
            print("Warning: pygame not available. Install with: pip install pygame")
            self.pygame_available = False
    
    def generate_sine_wave(self, frequency, duration, amplitude=0.5):
        """Generate a sine wave of specified frequency and duration"""
        frames = int(duration * self.sample_rate)
        arr = np.sin(2 * np.pi * frequency * np.linspace(0, duration, frames))
        return (arr * amplitude * 32767).astype(np.int16)
    
    def generate_swept_tone(self, start_freq, end_freq, duration, amplitude=0.5, initial_phase=0):
        """Generate a frequency-swept tone (chirp) with optional initial phase"""
        frames = int(duration * self.sample_rate)
        t = np.linspace(0, duration, frames)
        # Linear frequency sweep
        instantaneous_freq = start_freq + (end_freq - start_freq) * t / duration
        phase = initial_phase + 2 * np.pi * np.cumsum(instantaneous_freq) / self.sample_rate
        arr = np.sin(phase)
        # Return both the audio and the final phase for continuity
        final_phase = phase[-1] if len(phase) > 0 else initial_phase
        return (arr * amplitude * 32767).astype(np.int16), final_phase
    
    def generate_alternating_tone(self, freq1, freq2, duration1, duration2, total_duration, amplitude=0.5):
        """Generate alternating between two frequencies"""
        audio_data = np.array([], dtype=np.int16)
        current_time = 0
        use_freq1 = True
        
        while current_time < total_duration:
            if use_freq1:
                chunk_duration = min(duration1, total_duration - current_time)
                chunk = self.generate_sine_wave(freq1, chunk_duration, amplitude)
            else:
                chunk_duration = min(duration2, total_duration - current_time)
                chunk = self.generate_sine_wave(freq2, chunk_duration, amplitude)
            
            audio_data = np.concatenate([audio_data, chunk])
            current_time += chunk_duration
            use_freq1 = not use_freq1
        
        return audio_data
    
    def generate_pulsed_tone(self, frequency, on_duration, off_duration, total_duration, amplitude=0.5):
        """Generate a pulsed tone (on/off pattern)"""
        audio_data = np.array([], dtype=np.int16)
        current_time = 0
        pulse_on = True
        
        while current_time < total_duration:
            if pulse_on:
                chunk_duration = min(on_duration, total_duration - current_time)
                chunk = self.generate_sine_wave(frequency, chunk_duration, amplitude)
            else:
                chunk_duration = min(off_duration, total_duration - current_time)
                chunk = np.zeros(int(chunk_duration * self.sample_rate), dtype=np.int16)
            
            audio_data = np.concatenate([audio_data, chunk])
            current_time += chunk_duration
            pulse_on = not pulse_on
        
        return audio_data
    
    def _generate_burst_cycle(self, burst_generator_func, duration, remaining_time_check=1.5):
        """Helper method for generating 3-burst patterns with 1.5s gaps"""
        audio_data = np.array([], dtype=np.int16)
        
        # Generate 3 bursts with gaps between them
        for burst in range(3):
            burst_audio = burst_generator_func()
            audio_data = np.concatenate([audio_data, burst_audio])
            # Add 0.5s gap between bursts (not after the last one)
            if burst < 2:
                gap = np.zeros(int(0.5 * self.sample_rate), dtype=np.int16)
                audio_data = np.concatenate([audio_data, gap])
        
        # Add 1.5s final gap
        remaining_time = duration - (len(audio_data) / self.sample_rate)
        if remaining_time >= remaining_time_check:
            final_gap = np.zeros(int(remaining_time_check * self.sample_rate), dtype=np.int16)
            audio_data = np.concatenate([audio_data, final_gap])
        elif remaining_time > 0:
            partial_gap = np.zeros(int(remaining_time * self.sample_rate), dtype=np.int16)
            audio_data = np.concatenate([audio_data, partial_gap])
        
        return audio_data

    def generate_tone_audio(self, tone_number, duration=5.0):
        """Generate audio for a specific tone number"""
        lookup = AlertToneLookup()
        tone_data = lookup.get_tone_by_number(tone_number)
        
        if not tone_data:
            print(f"Tone #{tone_number} not found")
            return None
        
        print(f"Generating Tone #{tone_number}: {tone_data['description']}")
        
        # Parse the tone specifications and generate appropriate audio
        if tone_number == 1:  # 970Hz continuous
            return self.generate_sine_wave(970, duration)
        
        elif tone_number == 2:  # 800Hz/970Hz @ 2Hz
            return self.generate_alternating_tone(800, 970, 0.25, 0.25, duration)
        
        elif tone_number == 3:  # 800Hz – 970Hz @ 1Hz
            # @ 1Hz means 1 complete sweep per second, so each sweep takes 1 second
            sweep_duration = 1.0  # 1 second per sweep
            audio_data = np.array([], dtype=np.int16)
            current_time = 0
            
            while current_time < duration:
                remaining_time = duration - current_time
                if remaining_time >= sweep_duration:
                    # Full sweep
                    sweep, _ = self.generate_swept_tone(800, 970, sweep_duration)
                    audio_data = np.concatenate([audio_data, sweep])
                    current_time += sweep_duration
                elif remaining_time > 0:
                    # Partial sweep
                    full_sweep, _ = self.generate_swept_tone(800, 970, sweep_duration)
                    samples_needed = int(remaining_time * self.sample_rate)
                    partial_sweep = full_sweep[:samples_needed]
                    audio_data = np.concatenate([audio_data, partial_sweep])
                    break
                    
            return audio_data[:int(duration * self.sample_rate)]
        
        elif tone_number == 4:  # 970Hz 1s OFF/1s ON
            return self.generate_pulsed_tone(970, 1.0, 1.0, duration)
        
        elif tone_number == 5:  # 970Hz, 0.5s/ 630Hz, 0.5s
            return self.generate_alternating_tone(970, 630, 0.5, 0.5, duration)
        
        elif tone_number == 6:  # 554Hz, 0.1s/ 440Hz, 0.4s (AFNOR)
            return self.generate_alternating_tone(554, 440, 0.1, 0.4, duration)
        
        elif tone_number == 7:  # 500 – 1200Hz, 3.5s/ 0.5s OFF (Dutch Slow Whoop)
            cycle_duration = 4.0  # 3.5s sweep + 0.5s silence = 4s cycle
            cycles = max(1, int(duration / cycle_duration))
            audio_data = np.array([], dtype=np.int16)
            
            for cycle in range(cycles):
                # Add sweep
                sweep, _ = self.generate_swept_tone(500, 1200, 3.5)
                audio_data = np.concatenate([audio_data, sweep])
                
                # Add silence gap (check remaining time first)
                remaining_time = duration - (len(audio_data) / self.sample_rate)
                if remaining_time >= 0.5:
                    silence = np.zeros(int(0.5 * self.sample_rate), dtype=np.int16)
                    audio_data = np.concatenate([audio_data, silence])
                elif remaining_time > 0:
                    # Add partial silence if there's remaining time
                    partial_silence = np.zeros(int(remaining_time * self.sample_rate), dtype=np.int16)
                    audio_data = np.concatenate([audio_data, partial_silence])
                    break
                    
            return audio_data[:int(duration * self.sample_rate)]  # Trim to exact duration
        
        elif tone_number == 8:  # 420Hz 0.6s ON/0.6s OFF (AS1670 Alert)
            return self.generate_pulsed_tone(420, 0.6, 0.6, duration)
        
        elif tone_number == 9:  # 1000 - 2500Hz, 0.5s/ 0.5s OFF x 3/1.5s OFF (AS1670 Evacuation)
            cycles = max(1, int(duration / self.BURST_CYCLE_DURATION))
            audio_data = np.array([], dtype=np.int16)
            
            for cycle in range(cycles):
                # Generate one complete burst cycle
                burst_cycle = self._generate_burst_cycle(
                    lambda: self.generate_swept_tone(1000, 2500, 0.5)[0], 
                    duration - (len(audio_data) / self.sample_rate)
                )
                audio_data = np.concatenate([audio_data, burst_cycle])
                
                # Check if we have enough time for another complete cycle
                if len(audio_data) / self.sample_rate >= duration - self.BURST_CYCLE_DURATION:
                    break
                    
            return audio_data[:int(duration * self.sample_rate)]  # Trim to exact duration
        
        elif tone_number == 10:  # 550Hz/440Hz @ 0.5Hz
            return self.generate_alternating_tone(550, 440, 1.0, 1.0, duration)
        
        elif tone_number == 11:  # 970Hz, 0.5s ON/0.5s OFF x 3/ 1.5s OFF (ISO 8201)
            cycles = max(1, int(duration / self.BURST_CYCLE_DURATION))
            audio_data = np.array([], dtype=np.int16)
            
            for cycle in range(cycles):
                # Generate one complete burst cycle  
                burst_cycle = self._generate_burst_cycle(
                    lambda: self.generate_sine_wave(970, 0.5),
                    duration - (len(audio_data) / self.sample_rate)
                )
                audio_data = np.concatenate([audio_data, burst_cycle])
                
                # Check if we have enough time for another complete cycle
                if len(audio_data) / self.sample_rate >= duration - self.BURST_CYCLE_DURATION:
                    break
                    
            return audio_data[:int(duration * self.sample_rate)]  # Trim to exact duration
        
        elif tone_number == 13:  # 1200Hz – 500Hz @ 1Hz (DIN 33 404)
            # @ 1Hz means 1 complete sweep per second, so each sweep takes 1 second
            sweep_duration = 1.0  # 1 second per sweep
            audio_data = np.array([], dtype=np.int16)
            current_time = 0
            
            while current_time < duration:
                remaining_time = duration - current_time
                if remaining_time >= sweep_duration:
                    # Full sweep
                    sweep, _ = self.generate_swept_tone(1200, 500, sweep_duration)
                    audio_data = np.concatenate([audio_data, sweep])
                    current_time += sweep_duration
                elif remaining_time > 0:
                    # Partial sweep
                    full_sweep, _ = self.generate_swept_tone(1200, 500, sweep_duration)
                    samples_needed = int(remaining_time * self.sample_rate)
                    partial_sweep = full_sweep[:samples_needed]
                    audio_data = np.concatenate([audio_data, partial_sweep])
                    break
                    
            return audio_data[:int(duration * self.sample_rate)]
        
        elif tone_number == 14:  # 400Hz continuous
            return self.generate_sine_wave(400, duration)
        
        elif tone_number == 15:  # 550Hz, 0.7s/1000Hz, 0.33s
            return self.generate_alternating_tone(550, 1000, 0.7, 0.33, duration)
        
        elif tone_number == 16:  # 1500Hz – 2700Hz @ 3Hz
            # @ 3Hz means 3 complete sweeps per second, so each sweep takes 1/3 second
            sweep_duration = 1.0 / 3.0  # 0.333 seconds per sweep
            audio_data = np.array([], dtype=np.int16)
            current_time = 0
            
            while current_time < duration:
                remaining_time = duration - current_time
                if remaining_time >= sweep_duration:
                    # Full sweep
                    sweep, _ = self.generate_swept_tone(1500, 2700, sweep_duration)
                    audio_data = np.concatenate([audio_data, sweep])
                    current_time += sweep_duration
                elif remaining_time > 0:
                    # Partial sweep
                    full_sweep, _ = self.generate_swept_tone(1500, 2700, sweep_duration)
                    samples_needed = int(remaining_time * self.sample_rate)
                    partial_sweep = full_sweep[:samples_needed]
                    audio_data = np.concatenate([audio_data, partial_sweep])
                    break
                    
            return audio_data[:int(duration * self.sample_rate)]
        
        elif tone_number == 12:  # 2850Hz, 0.5s ON/0.5s OFF x 3/1.5s OFF (ISO 8201)
            cycles = max(1, int(duration / self.BURST_CYCLE_DURATION))
            audio_data = np.array([], dtype=np.int16)
            
            for cycle in range(cycles):
                # Generate one complete burst cycle - same pattern as tone 11 but 2850Hz
                burst_cycle = self._generate_burst_cycle(
                    lambda: self.generate_sine_wave(2850, 0.5),
                    duration - (len(audio_data) / self.sample_rate)
                )
                audio_data = np.concatenate([audio_data, burst_cycle])
                
                # Check if we have enough time for another complete cycle
                if len(audio_data) / self.sample_rate >= duration - self.BURST_CYCLE_DURATION:
                    break
                    
            return audio_data[:int(duration * self.sample_rate)]  # Trim to exact duration
        
        elif tone_number == 28:  # 500 - 1200Hz, 0.5s/ 0.5s OFF x 3/1.5s OFF (AS1670 Evacuation variant)
            cycles = max(1, int(duration / self.BURST_CYCLE_DURATION))
            audio_data = np.array([], dtype=np.int16)
            
            for cycle in range(cycles):
                # Generate one complete burst cycle - same pattern as tone 9 but 500-1200Hz
                burst_cycle = self._generate_burst_cycle(
                    lambda: self.generate_swept_tone(500, 1200, 0.5)[0],
                    duration - (len(audio_data) / self.sample_rate)
                )
                audio_data = np.concatenate([audio_data, burst_cycle])
                
                # Check if we have enough time for another complete cycle
                if len(audio_data) / self.sample_rate >= duration - self.BURST_CYCLE_DURATION:
                    break
                    
            return audio_data[:int(duration * self.sample_rate)]  # Trim to exact duration
        
        elif tone_number == 17:  # 750Hz continuous
            return self.generate_sine_wave(750, duration)
        
        elif tone_number == 18:  # 2400Hz continuous
            return self.generate_sine_wave(2400, duration)
        
        elif tone_number == 19:  # 660Hz continuous
            return self.generate_sine_wave(660, duration)
        
        elif tone_number == 20:  # 660Hz 1.8s ON/1.8s OFF
            return self.generate_pulsed_tone(660, 1.8, 1.8, duration)
        
        elif tone_number == 21:  # 660Hz 0.15s ON/0.15s OFF (fast pulse)
            return self.generate_pulsed_tone(660, 0.15, 0.15, duration)
        
        elif tone_number == 22:  # 510Hz, 0.25s/ 610Hz, 0.25s
            return self.generate_alternating_tone(510, 610, 0.25, 0.25, duration)
        
        elif tone_number == 23:  # 800/1000Hz 0.5s each (1Hz)
            return self.generate_alternating_tone(800, 1000, 0.5, 0.5, duration)
        
        elif tone_number == 24:  # 250Hz – 1200Hz @ 12Hz
            # @ 12Hz means 12 complete sweeps per second, so each sweep takes 1/12 second
            sweep_duration = 1.0 / 12.0  # 0.083 seconds per sweep
            audio_data = np.array([], dtype=np.int16)
            current_time = 0
            
            while current_time < duration:
                remaining_time = duration - current_time
                if remaining_time >= sweep_duration:
                    # Full sweep
                    sweep, _ = self.generate_swept_tone(250, 1200, sweep_duration)
                    audio_data = np.concatenate([audio_data, sweep])
                    current_time += sweep_duration
                elif remaining_time > 0:
                    # Partial sweep
                    full_sweep, _ = self.generate_swept_tone(250, 1200, sweep_duration)
                    samples_needed = int(remaining_time * self.sample_rate)
                    partial_sweep = full_sweep[:samples_needed]
                    audio_data = np.concatenate([audio_data, partial_sweep])
                    break
                    
            return audio_data[:int(duration * self.sample_rate)]
        
        elif tone_number == 25:  # 500Hz – 1200Hz @ 0.33Hz
            # @ 0.33Hz means 0.33 cycles per second, so each cycle (up+down) takes 1/0.33 = 3.03 seconds
            # Each half-cycle (up or down) takes 1.515 seconds
            cycle_duration = 1.0 / 0.33  # 3.03 seconds per full cycle
            half_cycle_duration = cycle_duration / 2.0  # 1.515 seconds per half-cycle
            audio_data = np.array([], dtype=np.int16)
            current_time = 0
            current_phase = 0  # Track phase for continuity
            
            while current_time < duration:
                remaining_time = duration - current_time
                
                # Up sweep: 500Hz to 1200Hz
                if remaining_time >= half_cycle_duration:
                    up_sweep, current_phase = self.generate_swept_tone(500, 1200, half_cycle_duration, initial_phase=current_phase)
                    audio_data = np.concatenate([audio_data, up_sweep])
                    current_time += half_cycle_duration
                elif remaining_time > 0:
                    # Partial up sweep - calculate how far through the frequency range we should sweep
                    # in the remaining time at the correct rate
                    freq_range = 1200 - 500  # 700Hz range
                    progress = remaining_time / half_cycle_duration  # how far through the sweep (0-1)
                    end_freq = 500 + (freq_range * progress)  # actual end frequency
                    partial_up_sweep, current_phase = self.generate_swept_tone(500, end_freq, remaining_time, initial_phase=current_phase)
                    audio_data = np.concatenate([audio_data, partial_up_sweep])
                    break
                
                remaining_time = duration - current_time
                
                # Down sweep: 1200Hz to 500Hz (with phase continuity)
                if remaining_time >= half_cycle_duration:
                    down_sweep, current_phase = self.generate_swept_tone(1200, 500, half_cycle_duration, initial_phase=current_phase)
                    audio_data = np.concatenate([audio_data, down_sweep])
                    current_time += half_cycle_duration
                elif remaining_time > 0:
                    # Partial down sweep - calculate how far through the frequency range we should sweep
                    freq_range = 1200 - 500  # 700Hz range
                    progress = remaining_time / half_cycle_duration  # how far through the sweep (0-1)
                    end_freq = 1200 - (freq_range * progress)  # actual end frequency
                    partial_down_sweep, current_phase = self.generate_swept_tone(1200, end_freq, remaining_time, initial_phase=current_phase)
                    audio_data = np.concatenate([audio_data, partial_down_sweep])
                    break
                    
            return audio_data[:int(duration * self.sample_rate)]
        
        elif tone_number == 26:  # 2400Hz – 2900Hz @ 9Hz
            # @ 9Hz means 9 complete sweeps per second, so each sweep takes 1/9 second
            sweep_duration = 1.0 / 9.0  # 0.111 seconds per sweep
            audio_data = np.array([], dtype=np.int16)
            current_time = 0
            
            while current_time < duration:
                remaining_time = duration - current_time
                if remaining_time >= sweep_duration:
                    # Full sweep
                    sweep, _ = self.generate_swept_tone(2400, 2900, sweep_duration)
                    audio_data = np.concatenate([audio_data, sweep])
                    current_time += sweep_duration
                elif remaining_time > 0:
                    # Partial sweep
                    full_sweep, _ = self.generate_swept_tone(2400, 2900, sweep_duration)
                    samples_needed = int(remaining_time * self.sample_rate)
                    partial_sweep = full_sweep[:samples_needed]
                    audio_data = np.concatenate([audio_data, partial_sweep])
                    break
                    
            return audio_data[:int(duration * self.sample_rate)]
        
        elif tone_number == 27:  # 2400Hz – 2900Hz @ 3Hz
            # @ 3Hz means 3 complete sweeps per second, so each sweep takes 1/3 second
            sweep_duration = 1.0 / 3.0  # 0.333 seconds per sweep
            audio_data = np.array([], dtype=np.int16)
            current_time = 0
            
            while current_time < duration:
                remaining_time = duration - current_time
                if remaining_time >= sweep_duration:
                    # Full sweep
                    sweep, _ = self.generate_swept_tone(2400, 2900, sweep_duration)
                    audio_data = np.concatenate([audio_data, sweep])
                    current_time += sweep_duration
                elif remaining_time > 0:
                    # Partial sweep
                    full_sweep, _ = self.generate_swept_tone(2400, 2900, sweep_duration)
                    samples_needed = int(remaining_time * self.sample_rate)
                    partial_sweep = full_sweep[:samples_needed]
                    audio_data = np.concatenate([audio_data, partial_sweep])
                    break
                    
            return audio_data[:int(duration * self.sample_rate)]
        
        elif tone_number == 31:  # 800Hz, 0.25s ON/1s OFF (short pulse, long gap)
            return self.generate_pulsed_tone(800, 0.25, 1.0, duration)
        
        elif tone_number == 29:  # 800Hz – 970Hz @ 9Hz
            # @ 9Hz means 9 complete sweeps per second, so each sweep takes 1/9 second
            sweep_duration = 1.0 / 9.0  # 0.111 seconds per sweep
            audio_data = np.array([], dtype=np.int16)
            current_time = 0
            
            while current_time < duration:
                remaining_time = duration - current_time
                if remaining_time >= sweep_duration:
                    # Full sweep
                    sweep, _ = self.generate_swept_tone(800, 970, sweep_duration)
                    audio_data = np.concatenate([audio_data, sweep])
                    current_time += sweep_duration
                elif remaining_time > 0:
                    # Partial sweep
                    full_sweep, _ = self.generate_swept_tone(800, 970, sweep_duration)
                    samples_needed = int(remaining_time * self.sample_rate)
                    partial_sweep = full_sweep[:samples_needed]
                    audio_data = np.concatenate([audio_data, partial_sweep])
                    break
                    
            return audio_data[:int(duration * self.sample_rate)]
        
        elif tone_number == 30:  # 800Hz – 970Hz @ 3Hz
            # @ 3Hz means 3 complete sweeps per second, so each sweep takes 1/3 second
            sweep_duration = 1.0 / 3.0  # 0.333 seconds per sweep
            audio_data = np.array([], dtype=np.int16)
            current_time = 0
            
            while current_time < duration:
                remaining_time = duration - current_time
                if remaining_time >= sweep_duration:
                    # Full sweep
                    sweep, _ = self.generate_swept_tone(800, 970, sweep_duration)
                    audio_data = np.concatenate([audio_data, sweep])
                    current_time += sweep_duration
                elif remaining_time > 0:
                    # Partial sweep
                    full_sweep, _ = self.generate_swept_tone(800, 970, sweep_duration)
                    samples_needed = int(remaining_time * self.sample_rate)
                    partial_sweep = full_sweep[:samples_needed]
                    audio_data = np.concatenate([audio_data, partial_sweep])
                    break
                    
            return audio_data[:int(duration * self.sample_rate)]
        
        elif tone_number == 32:  # 500Hz – 1200Hz, 3.75s/0.25s OFF (AS2220)
            cycle_duration = 4.0  # 3.75s sweep + 0.25s silence = 4s cycle
            audio_data = np.array([], dtype=np.int16)
            current_time = 0
            
            while current_time < duration:
                # Add sweep - check remaining time first
                remaining_time = duration - current_time
                if remaining_time >= 3.75:
                    # Full sweep
                    sweep, _ = self.generate_swept_tone(500, 1200, 3.75)
                    audio_data = np.concatenate([audio_data, sweep])
                    current_time += 3.75
                elif remaining_time > 0:
                    # Partial sweep - generate at normal rate but only take what we need
                    # Generate a full sweep at normal rate, then trim to remaining time
                    full_sweep, _ = self.generate_swept_tone(500, 1200, 3.75)
                    samples_needed = int(remaining_time * self.sample_rate)
                    partial_sweep = full_sweep[:samples_needed]
                    audio_data = np.concatenate([audio_data, partial_sweep])
                    break
                
                # Add silence gap if there's still time
                remaining_time = duration - current_time
                if remaining_time >= 0.25:
                    silence = np.zeros(int(0.25 * self.sample_rate), dtype=np.int16)
                    audio_data = np.concatenate([audio_data, silence])
                    current_time += 0.25
                elif remaining_time > 0:
                    # Partial silence
                    partial_silence = np.zeros(int(remaining_time * self.sample_rate), dtype=np.int16)
                    audio_data = np.concatenate([audio_data, partial_silence])
                    break
                    
            return audio_data[:int(duration * self.sample_rate)]  # Trim to exact duration
        
        else:
            # Default: generate a simple continuous tone for unimplemented patterns
            # Extract frequency from description
            freq = self.extract_primary_frequency(tone_data['frequency'])
            print(f"Using simplified continuous tone at {freq}Hz for tone #{tone_number}")
            return self.generate_sine_wave(freq, duration)
    
    def generate_burst_pattern_sweep(self, start_freq, end_freq, sweep_duration, off_duration, bursts, burst_gap):
        """Generate burst pattern with frequency sweeps"""
        burst_audio = np.array([], dtype=np.int16)
        for _ in range(bursts):
            # Swept tone
            sweep, _ = self.generate_swept_tone(start_freq, end_freq, sweep_duration)
            burst_audio = np.concatenate([burst_audio, sweep])
            # Off period (except for last burst)
            if _ < bursts - 1:
                off_chunk = np.zeros(int(off_duration * self.sample_rate), dtype=np.int16)
                burst_audio = np.concatenate([burst_audio, off_chunk])
        
        # Add burst gap
        gap_chunk = np.zeros(int(burst_gap * self.sample_rate), dtype=np.int16)
        return np.concatenate([burst_audio, gap_chunk])
    
    def extract_primary_frequency(self, freq_string):
        """Extract the primary frequency from a frequency string"""
        # Look for the first number followed by Hz
        match = re.search(r'(\d+)Hz', freq_string)
        if match:
            return int(match.group(1))
        return 1000  # Default fallback
    
    def play_tone(self, tone_number, duration=5.0):
        """Play a specific tone"""
        if not self.pygame_available:
            print("Cannot play audio: pygame not available")
            return
        
        audio_data = self.generate_tone_audio(tone_number, duration)
        if audio_data is None:
            return
        
        # Convert mono to stereo for pygame
        stereo_data = np.column_stack((audio_data, audio_data))
        
        # Play the audio
        try:
            import pygame
            sound = pygame.sndarray.make_sound(stereo_data)
            print(f"Playing tone #{tone_number} for {duration} seconds...")
            sound.play()
            time.sleep(duration)
            sound.stop()
        except Exception as e:
            print(f"Error playing audio: {e}")
    
    def stop_tone(self):
        """Stop currently playing tone"""
        if self.pygame_available:
            try:
                import pygame
                pygame.mixer.stop()
            except:
                pass


# Interactive Menu System
def display_menu():
    """Display the main menu options"""
    print("\n" + "="*60)
    print("🔊 KLAXON SONOS SIMULATOR 🔊")
    print("="*60)
    print("📋 ALERT TONES (1-32):")
    print("="*60)

def main_menu():
    """Main interactive menu loop"""
    lookup = AlertToneLookup()
    generator = ToneGenerator()
    
    if not generator.pygame_available:
        print("⚠️  Warning: Audio not available. Install pygame: pip install pygame numpy")
    
    while True:
        display_menu()
        
        # Display all tones
        for i in range(1, 33):
            tone = lookup.get_tone_by_number(i)
            if tone:
                standard = f" [{tone['standard']}]" if tone['standard'] else ""
                print(f"{i:2d}. {tone['description']}{standard}")
                print(f"    DIP: {tone['dip_switches']} | Freq: {tone['frequency']}")
        
        print("\n" + "="*60)
        try:
            choice = input("Enter tone number to play (1-32) or 0 to exit: ").strip()
            
            if choice == '0':
                print("\n👋 Goodbye!")
                break
            elif choice.isdigit():
                tone_num = int(choice)
                if 1 <= tone_num <= 32:
                    tone_info = lookup.get_tone_by_number(tone_num)
                    if tone_info:
                        print(f"\nTone #{tone_num}: {tone_info['description']}")
                        print(f"Frequency: {tone_info['frequency']}")
                        print(f"DIP Switches: {tone_info['dip_switches']}")
                        if tone_info['standard']:
                            print(f"Standard: {tone_info['standard']}")
                        
                        duration_input = input("Duration in seconds (default 5): ").strip()
                        try:
                            duration = float(duration_input) if duration_input else 5.0
                            if duration <= 0:
                                print("❌ Duration must be positive")
                                continue
                            if duration > 60:
                                print("⚠️  Long duration - press Ctrl+C to stop early")
                        except ValueError:
                            print("❌ Invalid duration, using default 5 seconds")
                            duration = 5.0
                        
                        print(f"\n� Playing tone #{tone_num} for {duration} seconds...")
                        generator.play_tone(tone_num, duration)
                        print("✓ Playback complete!")
                else:
                    print("❌ Please enter a number between 1 and 32")
            else:
                print("❌ Please enter a valid number")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


# Example usage and demonstration
if __name__ == "__main__":
    main_menu()