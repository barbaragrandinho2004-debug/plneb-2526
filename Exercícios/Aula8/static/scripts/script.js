function apagar_conceito(designacao){
        $.ajax("/conceitos/" + designacao, {
            method: "DELETE",
            success: function(response){
                alert("Correu bem!")
                window.location.href= "/conceitos"
        },
        error:function(response){
            alert("Correu mal!")
            console.log(response)
    }
    });
    }