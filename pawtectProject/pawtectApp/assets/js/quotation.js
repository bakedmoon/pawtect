
$(function() {
    var breedData = [];
    var amountData = [];
    var agesGroup = [];
    var age_item ={}
    var breed_item = {}
    
    $.ajax({
      type: "GET",
      url: "/get-filter-quote-data/",
      success: function(data) {
        
        let breedItem = data.breed.breeds
        let amountItem = data.amounts
        
        for(let i in breedItem){
          var item = breedItem[i]
          item.label = item.name
          breedData.push(item)
        }

        for(let i in amountItem){
          var item = amountItem[i]
          item.label = item.amount
          amountData.push(item)
        }
       
        for (let age of data.ages) {
          age.label = age.age_range
          agesGroup.push(age);
        }

        $(".tags1").autocomplete({
        source: breedData,
        minLength:0,
        select:function(ui,item){
          breed_item = item.item
        }
      }).bind('focus', function() {     
        if(!$(this).val().trim())
              $(this).keydown();
      });

        $(".tags").autocomplete({
        source: agesGroup,
        minLength:0,
        select:function(ui,item){
          age_item = item.item
        }
      }).bind('focus', function() {     
        if(!$(this).val().trim())
              $(this).keydown();
      });
  
      $(".tags2").autocomplete({
        source: amountData, minLength:0
      }).bind('focus', function() {     
        if(!$(this).val().trim())
              $(this).keydown();
      });
      }
    });

    var url_string = location;
    var url = new URL(url_string);
    var breedCat = url.searchParams.get("category__icontains");
    var breedName = url.searchParams.get("name");
    var breedStart_age = url.searchParams.get("age__start_age__in");
    var breedStart_age_unit = url.searchParams.get("age__start_age_unit__in");
    var breedEnd_age = url.searchParams.get("age__end_age__in");
    var breedEnd_age_unit = url.searchParams.get("age__end_age_unit__in");
    var breedAge_range = url.searchParams.get("age");

    // For Web

    var query = "?pawtect-quote=1";
    $("#searchId").click((e) => {
       e.preventDefault()

    var age = $("#tags").val()
    var breed = $("#tags1").val();
    var amount = $("#tags2").val()
    
   
   
    if(breed_item.category == undefined){
      breed_item.category = breedCat ? breedCat : breed_item.category;
      breed_item.name = breedName ? breedName : breed_item.name;
      age_item.start_age = breedStart_age ? breedStart_age : age_item.start_age;
      age_item.start_age_unit = breedStart_age_unit ? breedStart_age_unit : age_item.start_age_unit;
      age_item.end_age = breedEnd_age ? breedEnd_age : age_item.end_age;
      age_item.end_age_unit = breedEnd_age_unit ? breedEnd_age_unit : age_item.end_age_unit;
      age_item.age_range = breedAge_range ? breedAge_range : age_item.age_range;
    }else{
      breed_item.category = breed_item.category ? breed_item.category : breedCat;
      breed_item.name = breed_item.name ;
      age_item.start_age = age_item.start_age ? age_item.start_age : breedStart_age;
      age_item.start_age_unit = age_item.start_age_unit ? age_item.start_age_unit : breedStart_age_unit;
      age_item.end_age = age_item.end_age ? age_item.end_age : breedEnd_age;
      age_item.end_age_unit = age_item.end_age_unit ? age_item.end_age_unit : breedEnd_age_unit;
      age_item.age_range = age_item.age_range ? age_item.age_range : breedAge_range;
    }
    
    if (age.length >= 1) {
      query += "&age__start_age__in="+age_item.start_age+"&age__start_age_unit__in="+age_item.start_age_unit+"&age__end_age__in="+age_item.end_age+"&age__end_age_unit__in="+age_item.end_age_unit+"&age="+age;
    }
    
    if (breed.length >= 1) {
      query += "&category__icontains="+breed_item.category+"&name="+breed;
    }

    if (amount.length >= 1) {
      query += "&coverage_amount__amount=" + amount;
    }
    location.href = "/quotation/" + query;
  });




  // For Mobile
  $("#searchIdMob").click((e) => {
    e.preventDefault()
    
    var age = $("#tagsMob").val()
    var breed = $("#tags1Mob").val();
    var amount = $("#tags2Mob").val()
 
  if(breed_item.category == undefined){
    breed_item.category = breedCat ? breedCat : breed_item.category;
    breed_item.name = breedName ? breedName : breed_item.name;
    age_item.start_age = breedStart_age ? breedStart_age : age_item.start_age;
    age_item.start_age_unit = breedStart_age_unit ? breedStart_age_unit : age_item.start_age_unit;
    age_item.end_age = breedEnd_age ? breedEnd_age : age_item.end_age;
    age_item.end_age_unit = breedEnd_age_unit ? breedEnd_age_unit : age_item.end_age_unit;
    age_item.age_range = breedAge_range ? breedAge_range : age_item.age_range;
  }else{
    breed_item.category = breed_item.category ? breed_item.category : breedCat;
    breed_item.name = breed_item.name ;
    age_item.start_age = age_item.start_age ? age_item.start_age : breedStart_age;
    age_item.start_age_unit = age_item.start_age_unit ? age_item.start_age_unit : breedStart_age_unit;
    age_item.end_age = age_item.end_age ? age_item.end_age : breedEnd_age;
    age_item.end_age_unit = age_item.end_age_unit ? age_item.end_age_unit : breedEnd_age_unit;
    age_item.age_range = age_item.age_range ? age_item.age_range : breedAge_range;
  }
  
  if (age.length >= 1) {
    query += "&age__start_age__in="+age_item.start_age+"&age__start_age_unit__in="+age_item.start_age_unit+"&age__end_age__in="+age_item.end_age+"&age__end_age_unit__in="+age_item.end_age_unit+"&age="+age;
  }
  
  if (breed.length >= 1) {
    query += "&category__icontains="+breed_item.category+"&name="+breed;
  }

  if (amount.length >= 1) {
    query += "&coverage_amount__amount=" + amount;
  }
  location.href = "/quotation/" + query;
});

  
  });