ModalView = require 'views/core/ModalView'
PlayGameDevLevelView = require './PlayGameDevLevelView'

module.exports = class PlayGameDevLevelModal extends ModalView
  id: 'play-game-dev-level-modal'
  template: require 'templates/play/level/play-game-dev-level-modal'
  modalWidthPercent: 99
  
  initialize: (options, @levelID, @sessionID) ->
  
  afterRender: ->
    @insertSubView(new PlayGameDevLevelView({ @supermodel }, @levelID, @sessionID ))
    super()
