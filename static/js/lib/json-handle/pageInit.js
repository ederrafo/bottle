/**
 * Created with PyCharm.
 * User: myth
 * Date: 13-1-15
 * Time: 下午2:41
 * To change this template use File | Settings | File Templates.
 */
JH.md.jsonH.language = document.documentElement.lang;


function startJsonH(sJson) {
    JH.md.jsonH(sJson);
}

function jsonH_error(sJson) {
    alert(sJson);
}

//var oJson = JH.md.JSON();


var oView = {
    context : this
};

var sJson = '';
var eJsonData = JH.e('#jsonData');

if(eJsonData.firstChild) {

    JH.md.jsonH(eJsonData.firstChild.data);

}else{

    //var aSearch = location.search.match(/[\W]enterValue=([^&]*).*/);
    //if(aSearch) {
    //sJson = decodeURIComponent(aSearch[1]);
    //startJsonH(sJson);
    //}else{


    if(config.mode === 'request') {
        var jsonH_Request = JH.request(oView);
        var getJsonStringRequest = jsonH_Request.create(JH.request.NS.jsonH, 'getJsonString', {succeed : function (oResponseData, oRequestData) {
            try{
                startJsonH(oResponseData.data);
            }
            catch(e) {
                jsonH_error(oResponseData.data);
            }
        }});
        try{
            getJsonStringRequest.request('first view');
        }catch(e) {
            JH.md.jsonH();
        }

    }else if(config.mode === 'script_string') {
        startJsonH(script_JsonString);
    }else{
        JH.md.jsonH();
    }

    //}





}



//var jsonH_transceiver = $.transceiver(oView);
//jsonH_transceiver.follow(JH.transceiver.NS.jsonH, 'getJsonString', function (oFireData, oListenData) {
//try{
//startJsonH(oResponseData.data);
//}
//catch(e) {
//jsonH_error(oResponseData.data);
//}
//});






