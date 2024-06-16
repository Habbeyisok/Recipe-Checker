import sys
from main import main 
import logging

def test_main_with_data_file(monkeypatch, capsys):
    inputs = iter(['1', '7'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    test_args = ["script.py", "--data-file", "sample.json"]
    monkeypatch.setattr(sys, 'argv', test_args)
    main()
    captured = capsys.readouterr()
    assert "Recipe: Cheese Toastie" in captured.out
    assert "You can make a maximum of 1 servings!" in captured.out
