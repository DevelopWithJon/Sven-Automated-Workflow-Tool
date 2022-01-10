function deleteRecord(RouteId) {
  fetch("/delete-record", {
    method: "POST",
    body: JSON.stringify({ RouteId: RouteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}