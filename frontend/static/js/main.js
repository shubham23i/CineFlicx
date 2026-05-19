async function searchMovie() {

    const movie = document
        .getElementById("searchInput")
        .value;

    const response = await fetch(
        `/recommendation/recommend/${movie}`
    );

    const data = await response.json();

    console.log(data);
}