// var data = {"nodes": [{"name": "\u7f8e\u56fd", "id": 20}, {"\u7eed\u822a\u529b_\u6d77\u91cc": "4300", "\u9690\u8eab\u80fd\u529b": "\u5177\u5907", "nation": "\u7f8e\u56fd", "\u6700\u9ad8\u822a\u884c\u901f\u5ea6_\u8282": "50.0", "\u6700\u5927\u6392\u6c34\u91cf_\u5428": "2784", "name": "\u5409\u4f5b\u5179\u53f7\u6218\u6597\u8230", "\u5403\u6c34_m": "4.27", "\u5c3a\u5bf8_m": "127.6", "\u6807\u51c6\u6392\u6c34\u91cf_\u5428": "2176", "\u8230\u5bbd_m": "31.6", "\u7c7b\u522b": "\u8230\u8239", "id": 22}, {"nation": "\u7f8e\u56fd", "\u673a\u7ffc\u9762\u79ef_m2": "42.7", "\u53d1\u52a8\u673a\u6570_\u4e2a": "1", "name": "F-35_a", "\u98de\u884c\u901f\u5ea6_\u9a6c\u8d6b": "1.6", "\u9ad8\u5ea6_m": "4.33", "\u957f\u5ea6_m": "15.67", "\u98de\u884c\u9ad8\u5ea6_m": "18288", "\u96f7\u8fbe\u6563\u5c04\u622a\u9762\u79ef_\u5e73\u65b9\u7c73": "0.55", "\u7ffc\u5c55_m": "10.7", "\u7c7b\u522b": "\u98de\u673a", "id": 42}, {"\u7eed\u822a\u529b_\u6d77\u91cc": "4300", "\u9690\u8eab\u80fd\u529b": "\u4e0d\u5177\u5907", "nation": "\u7f8e\u56fd", "\u6700\u9ad8\u822a\u884c\u901f\u5ea6_\u8282": "30.0", "\u6700\u5927\u6392\u6c34\u91cf_\u5428": "9200", "name": "\u9ea6\u514b\u574e\u8d1d\u5c14\u53f7\u5bfc\u5f39\u9a71\u9010\u8230", "\u5c3a\u5bf8_m": "155.3", "\u5403\u6c34_m": "9.3", "\u6807\u51c6\u6392\u6c34\u91cf_\u5428": "x", "\u8230\u5bbd_m": "20.4", "\u7c7b\u522b": "\u8230\u8239", "id": 23}, {"nation": "\u7f8e\u56fd", "\u673a\u7ffc\u9762\u79ef_m2": "78.04", "\u53d1\u52a8\u673a\u6570_\u4e2a": "2", "name": "F-22", "\u98de\u884c\u901f\u5ea6_\u9a6c\u8d6b": "1.15", "\u9ad8\u5ea6_m": "5.08", "\u957f\u5ea6_m": "18.92", "\u98de\u884c\u9ad8\u5ea6_m": "18000", "\u96f7\u8fbe\u6563\u5c04\u622a\u9762\u79ef_\u5e73\u65b9\u7c73": "0.1", "\u7ffc\u5c55_m": "13.56", "\u7c7b\u522b": "\u98de\u673a", "id": 62}], "links": [{"relationships": "have", "id": 20, "source": 20, "target": 22}, {"relationships": "have", "id": 22, "source": 20, "target": 42}, {"relationships": "have", "id": 21, "source": 20, "target": 23}, {"relationships": "have", "id": 23, "source": 20, "target": 62}]};
setInterval(function() 
    {
        new QWebChannel(qt.webChannelTransport, function(channel) 
        {

            var channel_showNode = channel.objects.channel_showNode;


            channel_showNode.toJS.connect(function(str) 
            {
                // d3.selectAll("svg").remove();
                //alert('1');
                var data = JSON.parse(str);
                draw(data);
            });    
        });  
    },1000);

// draw(data);
function draw(data){

    var nodes = data.nodes;
    var links = data.links;

    var nodes_index = [];
    var links_index = [];
    for(i in nodes){
        nodes_index.push(nodes[i]["id"]);
    }

    for(i in links){
        links_index.push(links[i]["id"]);
        var target = links[i]["target"];
        links[i]["target"] = nodes_index.indexOf(target);
        var source = links[i]["source"];
        links[i]["source"] = nodes_index.indexOf(source);
    }
//------------数据处理结束-------------------

    var width = 2000;
    var height = 1200;
    var marge = {top:10,bottom:10,left:10,right:10}

        
    //设置一个color的颜色比例尺，为了让不同的扇形呈现不同的颜色
    var colorScale = d3.scaleOrdinal()
        .domain(d3.range(8))
        // .domain(d3.range(nodes.length))
        .range(d3.schemeCategory10);

    //新建一个力导向图
    var forceSimulation = d3.forceSimulation()
        .force("link",d3.forceLink())
        .force("charge",d3.forceManyBody())
        .force("center",d3.forceCenter())
        .force("collision",d3.forceCollide(30));



    forceDirectedGraph(nodes,links);
    function forceDirectedGraph(nodes,links,flag = true)
    {
        d3.selectAll("svg").remove();
        var svg = d3.select('body').append("svg")
        .attr("width",width)
        .attr('height',height)

        var g = svg.append("g")
            .attr("transform","translate("+marge.top+","+marge.left+")");
        //alert("get into forceDirectedGraph");

        //初始化力导向图，也就是传入数据
        //生成节点数据

        forceSimulation.nodes(nodes);
        //alert(JSON.stringify(nodes));
        //生成边数据
        forceSimulation.force("link")
            .links(links)
            .distance(200);
        forceSimulation.alpha(1).restart();


        //设置图形的中心位置 
        if(flag){
            forceSimulation.force("center",d3.forceCenter());
            forceSimulation.force("center")
                .x(width/5)
                .y(height/5);
        }
        //有了节点和边的数据后，我们开始绘制
        //绘制边
        var paths = g.append("g")
            .selectAll("line")
            .data(links)
            .enter()
            .append("line")
            // .attr("stroke",function(d,i){
            //     return colorScale(i);
            // })
            .attr("stroke","#8d8d8d")
            .attr("stroke-width",1);
        var pathsText = g.append("g")
            .selectAll("text")
            .data(links)
            .enter()
            .append("text")
            .text(function(d){
                return d.relationships;
            })

        //绘制节点
        //老规矩，先为节点和节点上的文字分组
        var gs = g.selectAll(".circleText")
            .data(nodes)
            .enter()
            .append("g")
            // .attr("transform",function(d,i){
            //     var cirX = d.x;
            //     var cirY = d.y;
            //     return "translate("+cirX+","+cirY+")";
            // })
            .call(d3.drag()
                .on("start",started)
                .on("drag",dragged)
                .on("end",ended)
            )
            .attr("fill", function(d) {
						let index = 0
						switch(d.label){
							case ':ErrorPlan': break;
							case ':Run': index = 1;break;
							case ':N': index = 2;break;
							case ':TE': index=3; break;
							case ':TL': index=4; break;
							case ':TS': index=5; break;
							case ':Target': index=6; break;
							case ':V': index=7; break;
							default: index=7;break;
						}
						return colorScale(index)
					})
            .on("click",function(d){
                new QWebChannel(qt.webChannelTransport, function(channel){
                    var channel_showPicPro = channel.objects.channel_showPicPro;
                        // channel_showPicPro.JSSendMessage(d.name);
                        channel_showPicPro.JSSendMessage(d.id);

                    }); 
                })
            .on("dblclick",function(d){
                new QWebChannel(qt.webChannelTransport, function(channel){
                    var channel_expandNode = channel.objects.channel_expandNode;
                        // channel_expandNode.JSSendMessage(d.name);
                        channel_expandNode.JSSendMessage(d.id);

                    channel_expandNode.toJS.connect(function(str){
                        let data2 = JSON.parse(str);

                        $.each(data2.nodes,function(d){

                            new_node = data2.nodes[d];
                            if(nodes_index.indexOf(new_node['id']) == -1){
                                nodes.push(new_node);
                                nodes_index.push(new_node['id']);
                            }
                        });
                        $.each(data2.links,function(d){
                            new_link = data2.links[d];
                            if(links_index.indexOf(new_link['id']) == -1){
                                links_index.push(new_link['id']);
                                let target = new_link["target"];
                                new_link["target"] = nodes_index.indexOf(target);
                                let source = new_link["source"];
                                new_link["source"] = nodes_index.indexOf(source);
                                links.push((new_link));
                                //alert(JSON.stringify(new_link));
                            }
                        });
                        forceDirectedGraph(nodes,links,false);
                    }); 
                });
            });

            
        //绘制节点
        gs.append("circle")
            .attr("r",30)
            // .attr("fill",function(d,i){
            //     return colorScale(i);
            // })

        //文字
        gs.append("text")
            .style("fill","#000")
            .attr("dominant-baseline","middle")
            .attr("text-anchor", "middle")//在圆圈中加上数据
            .text(function(d){
                if(d.name.length > 6){
                    return d.name.substring(0,6) + '....';
                }
                return d.name;
                
            });


        forceSimulation.on("tick",ticked);//这个函数很重要，后面给出具体实现和说明
        forceSimulation.alpha(1).restart();
        function ticked(){
            paths
                .attr("x1",function(d){return d.source.x;})
                .attr("y1",function(d){return d.source.y;})
                .attr("x2",function(d){return d.target.x;})
                .attr("y2",function(d){return d.target.y;});
                
            pathsText
                .attr("x",function(d){
                return (d.source.x+d.target.x)/2;
            })
            .attr("y",function(d){
                return (d.source.y+d.target.y)/2;
            });
                
            gs
                .attr("transform",function(d) { return "translate(" + d.x + "," + d.y + ")"; });
        }
        function started(d){
            if(!d3.event.active){
                forceSimulation.alphaTarget(0.8).restart();
            }
            forceSimulation.force("center", null);
            d.fx = d.x;
            d.fy = d.y;
        }
        function dragged(d){

            d.fx = d3.event.x;
            d.fy = d3.event.y;
        }
        function ended(d){
            if(!d3.event.active){
                forceSimulation.alphaTarget(0);
            }
            d.fx = null;
            d.fy = null;

        }
    }
}