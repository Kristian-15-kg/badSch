import React, { useState, useEffect } from 'react';
import axios from 'axios';

const EventCalendar = () => {
    const [events, setEvents] = useState([]);
    const [currentWeek, setCurrentWeek] = useState(getCurrentWeek());
    const [currentYear, setCurrentYear] = useState(new Date().getFullYear());

    useEffect(() => {
        fetchEvents();
    }, [currentWeek, currentYear]);

    const fetchEvents = async () => {
        try {
            const response = await axios.get(`/api/events/?week=${currentWeek}&year=${currentYear}`);
            setEvents(response.data);
        } catch (error) {
            console.error('Error fetching events:', error);
        }
    };

    const handleVote = async (eventId) => {
        try {
            await axios.post(`/api/events/${eventId}/vote/`);
            fetchEvents(); // Refresh events after voting
        } catch (error) {
            if (error.response?.data?.error) {
                alert(error.response.data.error);
            }
        }
    };

    return (
        <div className="event-calendar">
            <div className="calendar-header">
                <button onClick={() => setCurrentWeek(currentWeek - 1)}>Previous Week</button>
                <h2>Week {currentWeek}</h2>
                <button onClick={() => setCurrentWeek(currentWeek + 1)}>Next Week</button>
            </div>
            
            <div className="events-grid">
                {events.map(event => (
                    <div key={event.id} className="event-card">
                        <h3>{formatDate(event.date)}</h3>
                        <p>Time: {event.time}</p>
                        <p>Court: {event.court_number}</p>
                        <div className="participants">
                            <h4>Playing ({event.votes.filter(v => v.status === 'playing').length}/6)</h4>
                            {event.votes
                                .filter(v => v.status === 'playing')
                                .map(vote => (
                                    <div key={vote.id}>{vote.user.username}</div>
                                ))
                            }
                            <h4>Standby</h4>
                            {event.votes
                                .filter(v => v.status === 'standby')
                                .map(vote => (
                                    <div key={vote.id}>{vote.user.username}</div>
                                ))
                            }
                        </div>
                        <button onClick={() => handleVote(event.id)}>Vote</button>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default EventCalendar; 