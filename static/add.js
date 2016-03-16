/**
 * Created by Lenmon on 16-3-10.
 */
function add()
{
    var adder1 =Number(document.form1.add1.value);

    var adder2 =Number(document.form1.add2.value);
    var result = adder1 +adder2;

    document.form1.result.value = result;

}