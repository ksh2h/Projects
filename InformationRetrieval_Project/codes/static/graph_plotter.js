function plot_graph(result)
{
  if( result["type"] == "bar" )
  {
    var trace =
    {
      x : result["x"],
      y : result["y"],
      type : "bar",
    };
    var layout = {
      title : result["title"],
      xaxis : {
        title : result["xlabel"]
      },
      yaxis : {
        title : result["ylabel"]
      }
    };

    var data = [trace];
    Plotly.newPlot('graph_view', data, layout);
  }

  else if( result["type"] == "pie" )
  {
    var trace =
    {
      labels : result["x"],
      values : result["y"],
      type : "pie",
    };
    var layout =
    {
      title : result["title"],
      height : 500,
      width : 1000
    };
    var data = [trace];
    Plotly.newPlot('graph_view', data, layout);
  }

  else if( result["type"] == "stacked" )
  {
    var data = [];
    for( var key in result['y'] )
    {
      var trace = {};
      trace["x"] = result["x"];
      trace["y"] = result["y"][key];
      trace["name"] = key;
      trace["type"] = "bar";
      data.push(trace);
    }

    var layout = {
      title : result["title"],
      barmode:'stack'
    };
    console.log(data);
    Plotly.newPlot('graph_view', data, layout);
  }

}
