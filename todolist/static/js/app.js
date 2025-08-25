document.addEventListener('DOMContentLoaded', () => {
    // HTML elementlerini seçme
    const newTaskInput = document.getElementById('new-task-input');
    const addTaskBtn = document.getElementById('add-task-btn');
    const taskList = document.getElementById('task-list');
    const clearCompletedBtn = document.getElementById('clear-completed-btn');
    const taskCountSpan = document.getElementById('task-count');
    const filterButtons = document.querySelectorAll('.filter-btn');

    let tasks = []; 
    let currentFilter = 'all';


    const renderTasks = () => {
        taskList.innerHTML = '';

        const filteredTasks = tasks.filter(task => {
            if (currentFilter === 'completed') return task.TaskCompleted;
            if (currentFilter === 'uncompleted') return !task.TaskCompleted;
            return true;
        });

        filteredTasks.forEach(task => {
            const li = document.createElement('li');
            li.className = `task-item ${task.TaskCompleted ? 'completed' : ''}`;
            li.innerHTML = `
                <input type="checkbox" class="task-checkbox" ${task.TaskCompleted ? 'checked' : ''} data-id="${task.TaskID}">
                <span class="task-text">${task.TaskName}</span>
                <div class="task-actions">
                    <button class="delete-btn" data-id="${task.TaskID}">Sil</button>
                </div>
            `;
            taskList.appendChild(li);
        });
        updateTaskCount();
    };


    const updateTaskCount = () => {
        const remainingTasks = tasks.filter(task => !task.TaskCompleted).length;
        taskCountSpan.textContent = `${remainingTasks} görev kaldı`;
    };


    const fetchTasks = async () => {
    try {
        const response = await fetch('/api/tasks/');
        if (!response.ok) {
            throw new Error('API isteği başarısız oldu.');
        }
        const data = await response.json();
        tasks = data;
        renderTasks();
    } catch (error) {
        console.error('Görevler yüklenirken hata:', error);

    }
    };
    fetchTasks();

addTaskBtn.addEventListener('click', async () => {
    const text = newTaskInput.value.trim();
    if (text) {
        try {
            const response = await fetch('/api/tasks/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ TaskName: text, TaskCompleted: false })
            });

            if (response.ok) { 
                const newTask = await response.json();
                tasks.push(newTask);
                newTaskInput.value = '';
                fetchTasks();

            } else {
                console.error('Yeni görev oluşturulamadı.');
            }
        } catch (error) {
            console.error('Görev eklenirken hata:', error);
        }
    }
});


taskList.addEventListener('click', async (e) => {

    const target = e.target;
    const id = target.dataset.id;
    console.log('Aranan ID:', id, typeof id);
    console.log(e.target);
    if (target.classList.contains('delete-btn')) {
        console.log('Görevler dizisi:', tasks);

        const response = await fetch(`/api/tasks/${id}/`, { method: 'DELETE' });
        

        if (response.ok) {

            tasks = tasks.filter(task => task.TaskID !== id);
            renderTasks();
        } else {

            console.error('Görev silme işlemi başarısız oldu.');
        }
    }
    if (target.classList.contains('task-checkbox')) {
        const task = tasks.find(t => t.TaskID === id);
        if (task) {
            const newCompletedStatus = !task.TaskCompleted;

                await fetch(`/api/tasks/${id}/`, {
                 method: 'PATCH',
                 headers: { 'Content-Type': 'application/json' },
                 body: JSON.stringify({ TaskCompleted: newCompletedStatus })
                });
                
            task.TaskCompleted = newCompletedStatus;
            renderTasks();
            }
        }    
   
});


    clearCompletedBtn.addEventListener('click', async () => {
        const response = await fetch(`/api/tasks/clear_completed/`, { method: 'DELETE' });
        

        if (response.ok) {

            
            renderTasks();
        } else {

            console.error('Görev silme işlemi başarısız oldu.');
        }
        tasks = tasks.filter(task => !task.TaskCompleted);
        renderTasks();
    });

 
    filterButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            filterButtons.forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            currentFilter = e.target.dataset.filter;
            renderTasks();
        });
    });


    fetchTasks();
});

