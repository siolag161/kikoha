(($) ->
  createInlineReplyForm = (event) ->
    #alert 'aa'
    event.preventDefault()
    $form = $("#postcomment").clone(true)
    $cs = $(this).parent().parent()
    $id =  $cs.parent().attr('id').split("-")[1]
    $form.find('.parent').val $id
    $form.attr('id', 'postcomment-'+$id)
    $cs.append $form
    $(this).hide()
    return
     
  resetForm = ($form) ->
    $($form[0].elements["comment"]).val ""
    $($form[0].elements["parent"]).val ""
    return
    
  cancelCommentForm = (event) ->
    event.preventDefault() if event
    $form = $(event.target).closest('form')
    $form.parent().find('a.reply').show() # show rep button
    $form.remove()
    return

  addComment = (data) ->
    $data_html = $('<li/>', {'id': 'comment-'+ data.comment_id}).append(
      data['html']
    )
    $parent_node = undefined
    if !data['parent_id']
      $parent_node = $("#start-comments")
    else
      $parent_node = $("#comment-" + data['parent_id'])
      
    if $parent_node.find('div.children').length != 0
      $last_child = $parent_node.find('ul.comments').first().children().last()
      $last_child.after($data_html)
    else
      $parent_node.append( $('<div/>', {'class': 'children'}).append(
        $('<ul/>', {'class': 'comments'}).append(
          $data_html
          )
      ))
    return $("#comment-" + data.comment_id)

  commentSuccess = ($form,data) ->
    resetForm $form
    $new_comment = addComment(data)
    $new_comment.hide().show(600)
    $form.parent().find('a.reply').show()
    return $new_comment

  ajaxComment = (form, args) ->
    onsuccess = args.onsuccess
    preview = !!args.preview
    return false  if form.commentBusy
    form.commentBusy = true
    $form = $(form)
    comment = $form.serialize()
    url = $form.attr("action")
    ajaxurl = $form.attr("ajax_action")

    $.ajax
      type: "POST"
      url: ajaxurl
      data: comment
      dataType: "json"
      success: (data) ->
        form.commentBusy = false
        #removeWaitAnimation $form
        #removeErrors $form
        if data.success
          $added = undefined
          $added = commentSuccess($form, data)
          args.onsuccess data.comment_id, data.object_id, \
                   data.is_moderated, $added  if onsuccess
          if data.parent_id
            #alert 'bunbun'
            $form.remove()
        else
          #commentFailure data
        $form.parent().find('a.reply').show() # show rep button
        return

      error: (data) ->
        form.commentBusy = false
        $form.parent().find('a.reply').show() # show rep button
        #removeWaitAnimation()
        return
       
  onCommentPosted = (comment_id, object_id, is_moderated, $comment) ->
    #alert( comment_id + " --- " + object_id + " - " \
       #+ is_moderated + " --- " + $comment)
       #
    $('html, body').animate({
      scrollTop: $('#comment-'+comment_id).offset().top }, 'slow')
    return false


  onCommentFormSubmit = (event) ->
    event.preventDefault()
    form = event.target

    ajaxComment(form, {
      onsuccess: onCommentPosted
    })

    return false
    
  setActiveInput = () ->
    active_input = this.name
   
  $(document).ready ->
    $("#start-comments").on "click", ".reply", createInlineReplyForm
    $("#submit-id-cancel").click cancelCommentForm

    commentform = $('form.comment-form')
    if ( commentform.length > 0 )
      commentform.find(':input').focus(setActiveInput).mousedown(setActiveInput)
      commentform.submit(onCommentFormSubmit)

    
    return

) window.jQuery
