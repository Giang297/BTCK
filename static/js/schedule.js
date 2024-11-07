document.addEventListener('DOMContentLoaded', () => {
    const days = ['mon', 'tue', 'wed', 'thu', 'fri'];
    const sessions = ['morning', 'afternoon'];
    const periods = [1, 2, 3, 4, 5];

    // Lấy dữ liệu từ API
    fetch('/api/schedule')
        .then(response => response.json())
        .then(scheduleData => {
            days.forEach((day, dayIndex) => {
                sessions.forEach((session) => {
                    periods.forEach((period) => {
                        const cellId = `${session}-${period}-${day}`;
                        const cell = document.getElementById(`${session}-${period}-${day}`);
                        let classContent = '';

                        for (let className in scheduleData) {
                            const schedule = scheduleData[className][day];
                            if (schedule && schedule.session === (session === 'morning' ? 'Sáng' : 'Chiều') && schedule.period === `Tiết ${period}`) {
                                classContent = `<div><strong>${schedule.subject}</strong> (${schedule.teacher})</div>`;
                            }
                        }
                        cell.innerHTML = classContent || '-';
                    });
                });
            });
        });
});
