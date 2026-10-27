---
title: "Lessons learned from first experience with Power Apps"
date: 2021-01-04 11:30:07 +0100
description: "Source: PowerApps official site Last months, I had the opportunity to create my first Power Apps application at work and it was also my first time working with Power Apps, I did not even try"
tags: [Microsoft, Power Platform]
archived: true
---

{% raw %}
![](https://mohamedsahbicom.files.wordpress.com/2021/01/powerapps_logo.png?w=521)

Source: PowerApps official [site](https://powerapps.microsoft.com/en-us/)

Last months, I had the opportunity to create my first Power Apps application at work and it was also my first time working with Power Apps, I did not even try a hello world app before (well, I've seen demos before). However, I work with Power Automate (Flow) and O365 quite often. Therefore, I am used to the environment and the available tools.

Power platform is a low-code tool for citizen developers. Meanwhile, I am used to the traditional software development. This blog post is from a point of view of a software engineer.

#### **Forget about DRY principle**

“Don’t Repeat Yourself” (DRY) is a common principle we use in software development. This principle is hard to apply when working with Power Apps. It does not support macros or shared methods/ expression.

How to get around it? Use the select function of a button or any component to make a shared function. Then you call **`select(buttonName)`** to invoke the function. Don’t forget to hide the button.

This is not my idea, I found it when solving this problem in a blog post that I could not find anymore. Credits goes to the unknown who helped me :/ . However, here is a similar one that you can follow to apply DRY principle. [Microsoft BI Tools: Power Apps Snack: Don't repeat yourself (microsoft-bitools.blogspot.com)](http://microsoft-bitools.blogspot.com/2020/04/power-apps-snack-dont-repeat-yourself.html) .

Keep on mind that you will have to repeat yourself from time to time because there is no other way to get it done.

#### **Error while Exporting  package**

This error occurs when you delete a Power Automate flow that was used by the app. To solve the problem, you have to remove the “unused flow” from data section. Good luck with finding the flow in case you use multiple ones, Microsoft decided to show the GUID of the flow without the name, and reference flows by name only in Power Apps.

Saving the changes will not make the problem disappear; you have to publish it because the export applies only to the live version (published version).

![](https://mohamedsahbicom.files.wordpress.com/2021/01/cannot_export_app.png)

Figure 1: Export Power App Package

#### **Renaming/Updating Power Automate flow**

The Power Platform team agreed on minimum integration and sync between Power Automate and Power Apps. When you rename a flow or add a new parameter, it does not propagate in the app. You have to remove the current one with the old name and then select it with the new name. It is a painful process, so try to name it correctly the first time.

#### **Adding a Power Automate flow makes code disappear**

It is like magic! When you add a new flow to OnSelect or any other function, it deletes the current code and it replaces it with **`flowName.Run(`** .I am not sure who thought that this can be a good idea.. Please copy your code before adding a flow. You will need this in case you renamed the flow or added a new parameter.

![](https://mohamedsahbicom.files.wordpress.com/2021/01/powerapps_new_flow_deletes_code.gif)

Figure 2: Add new flow to a Power App

#### **Power Automate ToolTip**

A product development goes through changes especially when working with Agile methodologies. You may have to add parameters to the flow. When using the flow in Power Apps, the tooltip does not support multiple arguments (I did not measure it, but I have to work with flows that have more than 6 arguments and up to 13 arguments). At one point, you don’t know which argument you are setting and you cannot call its name, because the tooltip will show non-clickable three dots.

![](https://mohamedsahbicom.files.wordpress.com/2021/01/powerautomate_tooltip.png)

Figure 3: Flow ToolTip

How to solve it? I did not find a concrete way, but it goes by FIFO order when creating the flow (populated with **[Ask in Power Apps](https://docs.microsoft.com/en-us/powerapps/maker/canvas-apps/using-logic-flows)**). In other words, if you add a new parameter, it will be the last one to set its value in the **flowName.Run(arg1,arg2,.., lastArg)**.

### **PowerBI visual**

One of the great options of Power Apps is Power Apps Visual, a canvas in Power BI report. It comes with its limitations of course, but some of them are not listed and I discovered them while developing the app.

#### **Not all metrics are refreshed**

Metrics with data type Number are refreshed whenever you interact with the report. I used dependent dropdown lists that change when clicking on a table or a matrix.

I wanted to use another metric with data type Text that would be displayed on my app. The idea is to refresh the text same as the case of the other metrics. However, it did not work. I tried to solve it with the help of Power BI experts in our team, but we could not make it work. The verdict is that metric with data type Text cannot refresh its value in the Power App Visual.

#### **PowerApps (visual) Data has size limit**

I needed to use multiple hierarchies in the app alongside some metrics. At one moment, the app canvas does not load in the report and when editing it in Power App Visual Studio, it did not load the recently binded data. When I remove the recently added hierarchies, it works again.

What is the size limits? Well, who knows! I asked in Power Apps forum, but I did not get an answer. So, keep binding data until you achieve the limit or try to keep it clean and bind the minimum. Also, avoid binding hierarchies and such types because the report will take more time to load.

![](https://mohamedsahbicom.files.wordpress.com/2021/01/powerappvisual_doestnotload.png)

Figure 4: Power App loading forever

I hope this blog post will help you a bit. One last recommendation, save your changes so often with comments.

Good luck with your Power app.
{% endraw %}
