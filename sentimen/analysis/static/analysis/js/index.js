let dataTable;
let dataTableIsInitialized = false;

const dataTableOptions = {
    columnDefs: [
        { className: "centered", targets: [0, 1, 2, 3 ] },
        { orderable: false, targets: [3] },
        { searchable: false, targets: [3] }
    ],
    pageLength: 4,
    // Set destroy to false if you don't want to destroy the existing instance
    destroy: false
};

const initDataTable = async () => {
    try {
        // Destroy existing instance if initialized
        if (dataTableIsInitialized) {
            dataTable.destroy();
        }

        // Fetch and display tweets
        await listTweets();

        // Initialize DataTable
        dataTable = $("#datatable-tweets").DataTable(dataTableOptions);

        // Mark as initialized
        dataTableIsInitialized = true;
    } catch (ex) {
        alert(ex);
    }
};

const listTweets = async () => {
    try {
        // Fetch tweet data
        const response = await fetch(`http://127.0.0.1:8000/input/list-tweet/`);
        const data = await response.json();

        // Create HTML content for table rows
        let content = "";
        data.items.forEach((tweet, index) => {
            content += `
                <tr>
                    <td>${index + 1}</td>
                    <td>${tweet.fields.username || ''}</td>
                    <td>${tweet.fields.full_text || ''}</td>
                    <td>
                        <a href='/delete/list-tweet/${tweet.fields.idt}' class='btn btn-sm btn-danger'><i class='fa-solid fa-trash-can'></i></a>
                    </td>
                </tr>`;
        });
        

        // Update the table body
        $("#tableBody_tweet").html(content);
    } catch (ex) {
        alert(ex);
    }
};

// Ensure the window event listener is asynchronous
window.addEventListener("load", async () => {
    await initDataTable();
});
