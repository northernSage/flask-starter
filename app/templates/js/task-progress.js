$(function () {
  var refreshIntervalId = setInterval(function () {
    $.ajax("{{ url_for('homepage.get_job_progress', task_id=task.id) }}").done(
      function (job) {
        var message = '';
        if (job['complete'] == true) {
          message = 'Done!'
          clearInterval(refreshIntervalId);
        } else {
          message = job['description'] + " " + job['progress'] + "%"
        }
        $(task_id = '#' + job['id'] + '-progress').text(message);
      }
    );
  }, 1500);
});
