var api_url = 'http://127.0.0.1:5000/energy/api';

var deleteIcon = function(cell, formatterParams){ //plain text value
    return '<img src="img/delete.png">';
};

//Build Tabulator
var machinesTable = new Tabulator("#machines-table", {
    layout:"fitDataTable",
    ajaxURL:api_url+"/machines",
    ajaxContentType:"json",
    progressiveLoad:"scroll",
    paginationSize:20,
    placeholder:"No Data Set",
    columns:[
        {title:"ID", field:"id", sorter:"number"},
        {title:"Title", field:"title", sorter:"string", editor:"input"},
        {title:"Power", field:"power", hozAlign:"center", sorter:"number", editor:"input"},
        {formatter:deleteIcon, hozAlign:"center", cellClick:function(e, cell){machineDelete(cell.getRow().getData().id)}},
    ],
});

machinesTable.on("cellEdited", function(cell){
    machineEdit(cell.getRow().getData());
});
   

//дожидаемся полной загрузки страницы
window.onload = function () {
	machinesTable.setData();

    //получаем идентификатор элемента
    var a = document.getElementById('show-machines-table');
    //вешаем на него событие
    a.onclick = function() {
        // Удаление всех дочерних элементов
        var element = document.getElementById('machines');
        while (element.firstChild) {
            element.removeChild(element.firstChild);
        }

        fetch(api_url + '/machines')
        .then((response) => {
        return response.json()
        })
        .then((data) => {
            createTable(data['data']);
        });
        //предотвращаем переход по ссылке href
        return false;
    }
}

function machineAdd(event) {
	// Prevent the form from submitting.
  event.preventDefault();
  // Collect Data
  const formData = new FormData(event.target);
  // Build the data object.
  const data = {};
  formData.forEach((value, key) => (data[key] = value));
  // Log the data.
  console.log(data);
  
  fetch(api_url + '/machines', {
  method: 'POST',
  headers: { 
                'Content-type': 'application/json'
            },
  body: JSON.stringify(data)
}).then((response) => { 
  // do something with response here... 
}).then((data) => {
      console.log(data);
	  machinesTable.setData();
   });
}


async function machineEdit(machine) {
    try {
        machine_id = machine.id;
        const response = await fetch(api_url + '/machines/' + machine_id, {
            method: 'PUT',
            headers: { 
                'Content-type': 'application/json'
            },
            body: JSON.stringify(machine)
        });
        
        if (!response.ok) {
            throw new Error(`Error! status: ${response.status}`);
        }

        const result = await response.json();
		console.log(result);
		machinesTable.setData();
        return result;

    }
    catch (err) {
        console.log(err);
    }
}

async function machineDelete(machine_id) {
    try {
        const response = await fetch(api_url + '/machines/' + machine_id, {
            method: 'DELETE',
        });
        
        if (!response.ok) {
            throw new Error(`Error! status: ${response.status}`);
        }

        const result = await response.json();
		console.log(result);
		machinesTable.setData();
        return result;

    }
    catch (err) {
        console.log(err);
    }
}


function createTable(array) {
    const table = document.createElement('table');
    table.id = 'table';
    const tbody = document.createElement('tbody');
    const thead = document.createElement('thead');
    thead.innerHTML = `<tr>
                <th>ID</th>
                <th>Title</th>
                <th>Power</th>
                <th>Edit</th>
                <th>Delete</th>
              </tr>`;
    table.append(thead);
    table.append(tbody);

    for (let i = 0; i < array.length; i++) {
        let tr = document.createElement('tr');
        tr.innerHTML = `<td>${array[i].id}</td>
        <td>${array[i].title}</td>
        <td>${array[i].power}</td>
        <td><img src="img/edit.png"></td>
        <td><a href="#" onclick="event.preventDefault(); machineDelete(${array[i].id});"><img src="img/delete.png"></a></td>`;
        tbody.append(tr);
    }
    document.getElementById('machines').append(table);
}