<%inherit file='./layout.mako'/>

<%block name='title'>
 ${_('roadmap.title')} | ${_('application.name')}
</%block>

<div class="header" align="center">
  <h2><img class="logo-img" src="" width="52px" height="52px" alt="Scrolliris's Logo / TBD"></h2>
  <ul class="nav">
    <li><a class="overview link" href="/">${_('nav.header.overview')}</a></li>
    <li><a class="roadmap active link" href="${req.route_path('roadmap')}">${_('nav.header.roadmap')}</a></li>
    <li><a class="newsletter link" href="${var['tinyletter_url']}">${_('nav.header.newsletter')}</a></li>
  </ul>
</div>

<div class="container" align="center">
  <div class="grid roadmap" align="center">
    <div class="row">
      <div class="col-8 off-4">
        <p>TBD</p>
      </div>
    </div>
</div>
