$(document).ready(function(){

        var WEBSOCKET_ROUTE = "/ws";

        if(window.location.protocol == "http:"){
            //localhost
            var ws = new WebSocket("ws://" + window.location.host + WEBSOCKET_ROUTE);
        }
        else if(window.location.protocol == "https:"){
            //Dataplicity
            var ws = new WebSocket("wss://" + window.location.host + WEBSOCKET_ROUTE);
        }

        ws.onopen = function(evt) {
            // $("#ws-status").html("Connected");
            // $("#ws-status").css("background-color", "#afa");
            // $("#server_light").val("ON");
            $("#signal").html("READY");
            $("#ws-status").html("Connected");
            $("#ws-status").css("background-color", "#afa");

            // Get current configuration
            
        };

        ws.onmessage = function(evt) {
            //console.log(evt);
            var sData = JSON.parse(evt.data);
            //console.log(sData);
            if (sData.info !== 'undefined'){
              //console.log(sData.info + "|" + )

              if (sData.info == 'hello'){
                r = sData.reply.toString();
                $("#HelloResponse").html(r);
              }

              //WHAT TO DO WHEN WE GET A MESSAGE FROM THE SERVER
              if (sData.info == 'timer'){
                m = sData.m.toString();
                s = sData.s.toString().padStart(2,"0");
                $("#timeLeft").html(m + ":" + s);
              }

              //LEDs
              // Activate LEDs
              if (sData.info == 'LEDsActive'){
                if (sData.active == "show") {
                  $("#ledBlock").show();
                  $("#hasLEDs").prop("checked", true);
                  $("#nPix").val(sData.nPix);
                }
                else {
                  $("#ledBlock").hide();
                  console.log("LED's not activated by server. You may need to install the neoPixel library (see http://github.com/lurbano/rpi-led-strip)");
                }
              }

              if (sData.info == 'resetBrightness'){
                let val = sData.brightness;
                $("#setBrightness").val(val);
              }
              if (sData.info == 'resetColor'){
                $("#setColor").val(sData.color);
              }
              //LEDs (END)

            };
        };

        ws.onclose = function(evt) {
            $("#ws-status").html("Disconnected");
            $("#ws-status").css("background-color", "#faa");
            $("#server_light").val("OFF");
        };

        //MESSAGES TO SEND TO THE SERVER

        $("#hello").click(function(){
            let msg = '{"what": "hello"}';
            ws.send(msg);
        });

        $("#timer").click(function(){
            let m = $("#timerMin").val();
            let s = $("#timerSec").val();
            let msg = '{"what": "timer", "minutes":'+ m + ', "seconds": '+ s + '}';
            ws.send(msg);
        });

        $("#reboot").click(function(){
            let check = confirm("Reboot Pi?");
            if (check){
              var msg = '{"what": "reboot"}';
              ws.send(msg);
            }
        });

        // LEDs
        $("#setColor").change(function(){
            let msg = {
              "what": "led",
              "todo": "setColor",
              "color": this.value
            }
            ws.send(JSON.stringify(msg));
        });
        $("#setBrightness").change(function(){
            let msg = {
              "what": "led",
              "todo": "setBrightness",
              "brightness": this.value
            }
            ws.send(JSON.stringify(msg));
        });
        $("#clearButton").click(function(){
            let msg = {
              "what": "led",
              "todo": "clear"
            }
            ws.send(JSON.stringify(msg));
        });
        // LEDs (END)

      });
