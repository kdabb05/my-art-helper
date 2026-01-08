import sys
import builtins
import pathlib

# Ensure project root is on sys.path so tests can import main.py
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import main

def test_mock_mode_prints(capsys, monkeypatch):
    # provide input '1' for the menu
    monkeypatch.setattr(builtins, 'input', lambda prompt='': '1')
    monkeypatch.setattr(sys, 'argv', ['main.py', '--mock'])
    main.main()
    captured = capsys.readouterr()
    assert 'Essential Materials' in captured.out
    assert 'Practical Tips' in captured.out
    assert 'Budget Upgrades' in captured.out
    assert 'Nice-to-Have Upgrades' in captured.out
